from django.urls import path

from api_core.apps.auth import views

urlpatterns = [
    path('login', views.login),
    path('test', views.test_token),
]
