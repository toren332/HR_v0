from django.contrib import admin
from django.urls import path
from profiles import views as profiles_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'account', profiles_views.AccountViewSet, 'account')
router.register('users', profiles_views.UserViewSet, basename='users')
router.register('profiles', profiles_views.ProfileViewSet, basename='profiles')
router.register('teachers', profiles_views.TeacherViewSet, basename='teachers')
router.register('students', profiles_views.StudentViewSet, basename='students')
router.register('groups', profiles_views.GroupViewSet, basename='groups')
router.register('lessons', profiles_views.LessonViewSet, basename='lessons')


urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),

]
