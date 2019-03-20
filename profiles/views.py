from django.contrib import auth

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import models
from . import serializers


class AccountViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['POST'])
    def signup(self, request):

        serializer = serializers.SignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        profile = serializer.save()

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        return Response(serializers.ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_authenticated:
            username, password = serializer.validated_data['username'], serializer.validated_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
        else:
            auth.logout(request)
            username, password = serializer.validated_data['username'], serializer.validated_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

        profile = models.Profile.objects.get(user_id=user.id)

        return Response(serializers.ProfileSerializer(profile).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            user = request.user
            auth.logout(request)
            response = {"logout from "+str(user.id): True}
        else:
            response ={"logout": False}
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()
