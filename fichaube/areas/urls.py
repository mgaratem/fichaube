from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import areas.views

app_name = 'areas'
    # nota de pancho, esto del app_name es MUY importante!

urlpatterns = [

    # html's, estos despues se eliminaran*************
    path('agregar_Area', views.testpancho01, name="agregar_Area"),
    path('editar_Area/<int:idArea>', views.testpancho02, name='editar_Area'),
    path('agregar_Especialidad', views.testpancho03, name="agregar_Especialidad"),
    path('editar_Especialidad/<int:idEspecialidad>/<int:idArea>', views.testpancho04, name="editar_Especialidad"),

    # controladores de Areas
    path('agregarArea', views.agregarArea, name="agregarArea"),
    path('ajax/validarArea', views.validarArea, name="validarArea"),
    path('lista_Areas', views.listarAreas, name="lista_Areas"),
    path('eliminarArea/<int:idArea>', views.eliminarArea, name="eliminarArea"),
    path('editarArea', views.editarArea, name="editarArea"),
    path('editar_Area/ajax/validarArea', views.validarArea, name="validarArea"), # esta URL deberia eliminarla, y aprovechar la de mas arriba usando regex !!!

    # controladores de Especialidades
    path('lista_Especialidades/<int:idArea>', views.listarEspecialidades, name="lista_Especialidades"),
    path('agregarEspecialidad', views.agregarEspecialidad, name="agregarEspecialidad"),
    path('ajax/validarEspecialidad', views.validarEspecialidad, name="validarEspecialidad"),
    path('eliminarEspecialidad/<int:idEspecialidad>/<int:idArea>', views.eliminarEspecialidad, name="eliminarEspecialidad"),
    path('editarEspecialidad', views.editarEspecialidad, name="editarEspecialidad"),
    re_path(r'^editar_Especialidad/[0-9]+/ajax/validarEspecialidad', views.validarEspecialidad, name="validarEspecialidad")
]
