from django.db import models
from django.contrib.auth.models import User


# ACCOUNTS BLOCK


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
        ('student', 'Student'),
        ('client', 'Client'),
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


class Client(models.Model):
    """Профиль клиента."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.profile.user.username


# OBJECTS BLOCK


class Faculty(models.Model):
    """Факультет."""
    name = models.CharField('Faculty name', max_length=150,
                            help_text='Faculty name', unique=True)

    def __str__(self):
        return 'Faculty: ' + self.name


class Stream(models.Model):
    """Поток."""
    name = models.CharField('Stream name', max_length=150,
                            help_text='Stream name', unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return 'Stream: ' + self.name


class Group(models.Model):
    """Группа."""
    name = models.CharField('name', max_length=150,
                            help_text='Group name', unique=True)
    is_primary = models.BooleanField('is_primary', default=False,
                                     help_text='Indicates is the group primary')

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        if self.stream:
            return 'Stream: ' + self.stream.name + ' ;Group: ' + self.name + '; verified: ' + str(self.is_primary)
        else:
            return 'Group: ' + self.name + '; verified: ' + str(self.is_primary)


class Lesson(models.Model):
    """Занятие."""
    name = models.CharField('lesson name', max_length=150, blank=False,
                            help_text='lesson name')

    TYPE_CHOICES = (
        ('class', 'class'),
        ('lecture', 'lecture')
    )
    type = models.CharField(choices=TYPE_CHOICES, default='class', max_length=7)
    primary_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, related_name='primary_teacher')
    secondary_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name='secondary_teacher')

    class Meta:
        unique_together = (("name", "type", "primary_teacher"),)

    def __str__(self):
        return self.name + ' - ' + self.type


class University(models.Model):
    """Университет."""
    name = models.CharField('university name', max_length=150, blank=False, unique=True,
                            help_text='university name')

    english_name = models.CharField('university english name', max_length=150, blank=False, unique=True,
                                    primary_key=True,
                                    help_text='university english name')  # нужно для использования PK

    description = models.CharField('university description', max_length=5000, blank=True,
                                   help_text='university description')

    def __str__(self):
        return self.name


class Building(models.Model):
    """Строение."""
    name = models.CharField('building name', max_length=150, blank=False, unique=True, primary_key=True,
                            help_text='building name')

    address = models.CharField('building address', max_length=5000, blank=True,
                               help_text='building address')

    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Auditory(models.Model):
    """Аудитория."""
    name = models.CharField('auditory name', max_length=50, blank=False, unique=True, primary_key=True,
                            help_text='auditory name')

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# TIMETABLE BLOCK

class Timetable(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE)


class TimetableItem(models.Model):
    """Событие в расписании."""
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    auditory = models.ForeignKey(Auditory, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    REPEAT_KIND = (
        ('once', 'Once'),
        ('every_second_week', 'Every_second_week'),
        ('every_week', 'Every_week'),
        ('every_workday_day5', 'Every_workday_day5'),
        ('every_workday_day6', 'Every_workday_day6'),
        ('every_day', 'Every_day'),
        ('custom', 'Custom'),
    )
    repeat = models.CharField(choices=REPEAT_KIND, default='once', max_length=7,
                              help_text='Repeat type for lesson')
    # TODO: создать exclude TimetableItem

    def __str__(self):
        return 'Lesson: ' + self.lesson.name + '; Teacher ' + self.lesson.primary_teacher.profile.user.username + \
               '; Auditory: ' + self.auditory.name + ' (' + self.auditory.building.name + '); Start time: ' + \
               str(self.start_time)


# OBJECTS TRASH BLOCK


class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("group", "student"),)

    def __str__(self):
        return 'Group: ' + self.group.name + '; Login: ' + self.student.profile.user.username


class LessonGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("group", "lesson"),)

    def __str__(self):
        return 'Group: ' + self.group.name + '; Lesson: ' + self.lesson.name
