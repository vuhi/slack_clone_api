from django.urls import path

from api_core.apps.experiment import views

urlpatterns = [
    # GET
    path('ping', views.ping),
    path('protected', views.protected_ping),
    path('generate-token', views.generate_token),
    path('error/normal', views.capture_normal_exception),
    path('error/api', views.capture_api_exception),
]
