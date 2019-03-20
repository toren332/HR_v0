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


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()

    @action(detail=True, methods=['POST'])
    def enter_group(self, request, pk=None):
        data = request.data
        data['student'] = pk
        serializer = serializers.StudentGroupSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student_group = serializer.save()

        return Response(serializers.StudentGroupSerializer(student_group).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def exit_group(self, request, pk=None):
        data = request.data
        data['student'] = pk
        if not models.StudentGroup.objects.filter(student=data['student'], group=data['group']):
            return Response(["there is no student " + str(data['student']) + " from group " + str(data['group'])], status=status.HTTP_400_BAD_REQUEST)
        student_group = models.StudentGroup.objects.get(student=data['student'], group=data['group'])
        student_group.delete()
        return Response(["student " + str(data['student']) + " exit from " + str(data['group'])], status=status.HTTP_200_OK)


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer
    queryset = models.Teacher.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
