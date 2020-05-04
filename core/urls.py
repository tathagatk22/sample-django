from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^health-check$', views.health_check),
]
