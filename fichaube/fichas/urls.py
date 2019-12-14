from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('crear_ficha/', views.crearFicha, name="crearFicha"),
    path('confirmacion_ficha/<int:id_alumno>', views.confirmarCreacionFicha, name="confirmarCreacionFicha"),
    path('crear_registro/<int:id_alumno>', views.crearRegistro, name="crearRegistro"),
]
