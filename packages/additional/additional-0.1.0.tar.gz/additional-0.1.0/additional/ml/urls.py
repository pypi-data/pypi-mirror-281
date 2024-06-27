"""
URL configuration for ml project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('credential.urls')),
    path('v1/', include('v1.urls')),
    path('', include('backend.urls')),
    path('', include('join.urls')),
    path('', include('ai.urls')),
]
