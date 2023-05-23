from django.urls import path, include

urlpatterns = [
    path('api/', include('estate_backend.api.urls', namespace='api')),
    path('api/drf-auth/', include('rest_framework.urls')),
]
