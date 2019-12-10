from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'permisos'

urlpatterns = [
    path('ceder_permiso/<int:id_alumno>', views.cederPermiso, name="cederPermiso"),
    path('revocar_permiso/<int:id_permiso>/<int:id_alumno>', views.revocarPermiso, name="revocarPermiso"),
]
