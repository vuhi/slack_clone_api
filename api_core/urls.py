from django.contrib import admin
from django.urls import path, include

from .apps.auth.urls import urlpatterns as auth_routes
from .apps.ping import views

urlpatterns = [
    path('api/', include([
        path('auth/', include(auth_routes)),
        path('ping/', views.ping),
    ])),
    path('admin/', admin.site.urls),
]
