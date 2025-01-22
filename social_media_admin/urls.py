"""
URL configuration for social_media_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from .views import admin_login, admin_logout


schema_view = get_schema_view(
   openapi.Info(
        title="Social Media Admin API",
        default_version='v1',
        description="API documentation for the Social Media Admin project",
        license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', admin_login, name='admin_login'),  # Admin login
    path('auth/logout/', admin_logout, name='admin_logout'), 
    path('users/', include('user_management.urls')),     
    path('content/', include('content_management.urls')),  # Content management
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Add media URL configurations for serving uploaded files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)