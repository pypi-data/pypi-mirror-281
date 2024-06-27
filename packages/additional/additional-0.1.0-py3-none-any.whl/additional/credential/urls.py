
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls

urlpatterns = [
    path('o/', include(oauth2_urls)),
]
