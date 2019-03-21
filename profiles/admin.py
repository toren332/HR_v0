from django.contrib import admin
from . import models

# ACCOUNTS BLOCK


admin.site.register(models.Profile)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Client)


# OBJECTS BLOCK


admin.site.register(models.Group)
admin.site.register(models.Lesson)
admin.site.register(models.University)
admin.site.register(models.Building)
admin.site.register(models.Auditory)


# OBJECTS TRASH BLOCK


admin.site.register(models.StudentGroup)
