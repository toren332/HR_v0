"""HR_v0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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


urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),

]
