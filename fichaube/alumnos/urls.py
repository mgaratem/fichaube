from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('crear_alumno/', views.crear_alumno, name="crear_alumno"),
    path('borrar_alumno/<int:id_alumno>', views.borrarAlumno, name="borrarAlumno"),
    path('actualizar_alumno/<int:id_alumno>', views.updateAlumno, name="updateAlumno"),
    path('ver_alumno/<int:id_alumno>', views.verAlumno, name="verAlumno"),
    path('listar_alumnos/', views.listarAlumnos, name="listarAlumnos"),
]
