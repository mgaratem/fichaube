from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# revisar esto, ya que tengo dudas con los import de views************************************************************************
import areas.views


urlpatterns = [
    path('home/', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # HANDLERS
    path('404/', views.handler404, name="404"),
    path('500/', views.handler500, name="500"),

    path('cambiar_pass/', views.cambiar_pass, name="cambiar_pass"),


    # html's, estos despues se eliminaran*************
    path('agregar-Area', areas.views.testpancho01, name="agregar-Area"),
    path('editar-Area/<int:idArea>', areas.views.testpancho02, name='editar-Area'),
    path('agregar-Especialidad', areas.views.testpancho03, name="agregar-Especialidad"),

    # controladores de Areas
    path('agregarArea', areas.views.agregarArea, name="agregarArea"),
    path('ajax/validarArea', areas.views.validarArea, name="validarArea"),
    path('lista-Areas', areas.views.listarAreas, name="lista-Areas"),
    path('eliminarArea/<int:idArea>', areas.views.eliminarArea, name="eliminarArea"),
    path('editarArea', areas.views.editarArea, name="editarArea"),
    path('editar-Area/ajax/validarArea', areas.views.validarArea, name="validarArea"), # esta URL deberia eliminarla, y aprovechar la de mas arriba usando regex !!!

    # controladores de Especialidades
    path('lista-Especialidades/<int:idArea>', areas.views.listarEspecialidades, name="lista-Especialidades"),
    path('agregarEspecialidad', areas.views.agregarEspecialidad, name="agregarEspecialidad")


]
