from django.contrib import admin
from django.urls import path
from api_v0 import urls
from django.conf.urls import include, url

from rest_framework import routers

router = routers.DefaultRouter()



urlpatterns = router.urls

urlpatterns += [
    url(r'^api/v0/', include(urls)),
    path('admin/', admin.site.urls),
]
