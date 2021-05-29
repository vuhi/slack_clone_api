from django.urls import path

from api_core.apps.auth import views

urlpatterns = [
    # POST
    path('register', views.register_user),
    path('login', views.login),
]
