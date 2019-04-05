from django.db.models import QuerySet


class ProfileQuerySet(QuerySet):
    def create(self, *args, **kwargs):
        """
        TODO: should be here

        if kind == 'student':
            student = models.Student.objects.create(profile_id=profile.user_id)
            student.save()
        elif kind == 'teacher':
            teacher = models.Teacher.objects.create(profile_id=profile.user_id)
            teacher.save()
        else:
            client = models.Client.objects.create(profile_id=profile.user_id)
            client.save()
        """
        return self.create(*args, **kwargs)
