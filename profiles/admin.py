from django.contrib import admin
from .models import Profile, Student, Teacher, StudentGroup

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentGroup)
