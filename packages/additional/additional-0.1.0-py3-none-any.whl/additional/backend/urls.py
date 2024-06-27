# auth0authorization/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('v1/public/', views.public),
    path('v1/private/', views.private),
    path('v1/private-scoped/', views.private_scoped),
]
