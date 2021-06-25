from django.urls import path

from api_core.apps.auth import views

urlpatterns = [
    # GET
    path('login/config', views.get_oauth_config),

    # POST
    path('register', views.register_user),
    path('login', views.login),
    path('login/oauth', views.oauth_login),
]
