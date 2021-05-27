from django.urls import path

from api_core.apps.experiment import views

urlpatterns = [
    # GET
    path('ping', views.ping),
    path('protected', views.protected_ping),
    path('generate-token', views.generate_token),
]
