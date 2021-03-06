from django.contrib import admin
from django.urls import include, path
from . import views
from .views import GeneratePdf
from .views import ReporteExcel

app_name = 'fichas'

urlpatterns = [
    path('crear_ficha/', views.crearFicha, name="crearFicha"),
    path('confirmacion_ficha/<int:id_alumno>', views.confirmarCreacionFicha, name="confirmarCreacionFicha"),
    path('crear_registro/<int:id_alumno>', views.crearRegistro, name="crearRegistro"),
    path('reportes/', views.reportes, name="reportes"),
    path('generarReporte', ReporteExcel.as_view(), name="generarReporte"),
    path('crear_pdf_ficha/<int:id_alumno>', GeneratePdf.as_view(), name="crearFichaPDF"),
    path('ver_registro/<int:id_registro>', views.verRegistro, name="verRegistro"),
]
