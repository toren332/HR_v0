from django.contrib import admin
from .models import Profile, Student, Teacher, StudentGroup, Group, Lesson

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(StudentGroup)
admin.site.register(Lesson)
