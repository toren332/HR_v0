from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField('first_name', max_length=40, blank=True,
                                  help_text='Account first name')
    middle_name = models.CharField('middle_name', max_length=40, blank=True,
                                   help_text='Account middle name')
    last_name = models.CharField('middle_name', max_length=40, blank=True,
                                 help_text='Account last name')
    is_verified = models.BooleanField('is_verified', default=False,
                                      help_text='Indicates account has been verified for identity')
    is_admin = models.BooleanField('is_admin', default=False,
                                   help_text='Indicates account has been admin for identity')
    PROFILE_KIND = (
        ('teacher', 'Teacher'),
        ('student', 'Student')
    )
    kind = models.CharField(choices=PROFILE_KIND, default='student', max_length=7,
                            help_text='Indicates account type student or teacher')

    def __str__(self):
        return self.user.username + '  –  ' + self.kind


class Student(models.Model):
    """Профиль студента."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.profile.user.username


class Teacher(models.Model):
    """Профиль учителя."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.profile.user.username


class Group(models.Model):
    """Группа."""
    name = models.CharField('name', max_length=150,
                            help_text='Group name', unique=True)
    is_primary = models.BooleanField('is_primary', default=False,
                                     help_text='Indicates is the group primary')

    def __str__(self):
        return 'Group: ' + self.name + '; verified: ' + str(self.is_primary)


class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("group", "student"),)

    def __str__(self):
        return 'Group: ' + self.group.name + '; Login: ' + self.student.user.username
