from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('crea_usuario/', views.crear_user, name='crear_user'),
    path('cambiar_pass/', views.cambiar_pass, name='cambiar_pass'),
]
