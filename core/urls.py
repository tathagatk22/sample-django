from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^health-check$', views.health_check),  # API to check health status
    url(r'^fetch-data$', views.fetch_data),  # API to fetch data
    url(r'^create-random-user$', views.create_user),  # API to create data
    url(r'^create-random-activity-periods$', views.create_activity_period),  # API to create data
]
