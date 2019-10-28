from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('crear_alumno/', views.crear_alumno, name="crear_alumno"),
]
