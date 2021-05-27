from django.contrib import admin
from django.urls import path, include

from .apps.auth.urls import urlpatterns as auth_routes
from .apps.experiment.urls import urlpatterns as experiment_routes

urlpatterns = [
    path('api/', include([
        path('auth/', include(auth_routes)),
        path('experiment/', include(experiment_routes)),
    ])),
    path('admin/', admin.site.urls),
]
