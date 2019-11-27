from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('crear_ficha/', views.crearFicha, name="crearFicha"),
]
