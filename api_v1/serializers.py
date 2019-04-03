from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from profiles import models
from django.db.models import Q

# ACCOUNTS BLOCK


class UserSerializer(serializers.ModelSerializer):
    # TODO: запретить удаление пользователя, ТЕ заменить на deactivate

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    # TODO: запретить удаление profile и редактирование User

    class Meta:
        model = models.Profile
        fields = ['user', 'first_name', 'middle_name', 'last_name', 'is_verified', 'is_admin', 'kind']


class TeacherSerializer(serializers.ModelSerializer):
    # TODO: запретить создание и удаление Teacher и редактирование Profile

    profile = serializers.PrimaryKeyRelatedField(queryset=models.Profile.objects.all(), required=False)

    class Meta:
        model = models.Teacher
        fields = ['profile', ]


class StudentSerializer(serializers.ModelSerializer):
    # TODO: запретить создание и удаление Student и редактирование Profile

    profile = serializers.PrimaryKeyRelatedField(queryset=models.Profile.objects.all(), required=False)

    class Meta:
        model = models.Student
        fields = ['profile', ]


class ClientSerializer(serializers.ModelSerializer):
    # TODO: запретить создание и удаление Client и редактирование Profile

    profile = serializers.PrimaryKeyRelatedField(queryset=models.Profile.objects.all(), required=False)

    class Meta:
        model = models.Student
        fields = ['profile', ]


# OBJECTS BLOCK


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('name', 'is_primary', 'id')


class LessonSerializer(serializers.ModelSerializer):
    # TODO: запретить ставить себя как второго учителя
    class Meta:
        model = models.Lesson
        fields = ('name', 'type', 'primary_teacher', 'secondary_teacher', 'id')


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lesson
        fields = ('name', 'description')


# OBJECTS TRASH BLOCK


class StudentGroupSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_student(student: models.Student) -> models.Student:
        if not models.Student.objects.filter(profile__user_id=student.profile.user_id):
            msg = 'There is no this student id'
            raise serializers.ValidationError(msg)
        return student

    def create(self, validated_data: dict) -> models.StudentGroup:
        student = validated_data.pop('student')
        group = validated_data.pop('group')

        student_group = models.StudentGroup(student=student, group=group)
        student_group.save()

        return student_group

    class Meta:
        model = models.StudentGroup
        fields = ('student', 'group')


# AUTHORIZATION/authentication BLOCK


class SignupSerializer(serializers.Serializer):
    PROFILE_KIND_CHOICES = models.Profile.PROFILE_KIND
    username = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)
    kind = serializers.ChoiceField(PROFILE_KIND_CHOICES, required=True)

    @staticmethod
    def validate_email(email: str) -> str:
        if User.objects.filter(email=email).exists():
            msg = 'Someone already has an account with the same e-mail address'
            raise serializers.ValidationError(msg)
        return email

    @staticmethod
    def validate_password(password: str) -> str:
        password_validation.validate_password(password)
        return password

    @staticmethod
    def validate_username(username: str) -> str:
        if User.objects.filter(username=username).exists():
            msg = 'Someone already has an account with the username'
            raise serializers.ValidationError(msg)
        return username

    def create(self, validated_data: dict) -> [User, int, dict]:
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        kind = validated_data.pop('kind')

        user = User()
        user.email = email
        user.set_password(password)
        user.is_active = True
        user.username = username
        user.save()

        profile = models.Profile.objects.create(user_id=user.id, kind=kind)
        profile.save()

        if kind == 'student':
            student = models.Student.objects.create(profile_id=profile.user_id)
            student.save()
        elif kind == 'teacher':
            teacher = models.Teacher.objects.create(profile_id=profile.user_id)
            teacher.save()
        else:
            client = models.Client.objects.create(profile_id=profile.user_id)
            client.save()
        return profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, data: dict) -> dict:
        username_or_email = data.get('username')
        password = data.get('password')

        user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if not user or not user.check_password(password):
            error_msg = 'The username / email or password is not correct'
            raise serializers.ValidationError(error_msg)

        if not user.is_active:
            error_msg = 'The account is disabled'
            raise serializers.ValidationError(error_msg)

        return data
