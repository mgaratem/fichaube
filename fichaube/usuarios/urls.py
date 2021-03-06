from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'usuarios'

urlpatterns = [
    #path('crear_user/', views.crear_user, name='crear_user'),
    path('cambiar_pass/', views.cambiarPass, name='cambiarPass'),
    path('crear_usuario/', views.crear_usuario, name="crear_usuario"),
    path('borrar_usuario/<int:id_usuario>', views.borrarUsuario, name="borrarUsuario"),
    path('actualizar_usuario/<int:id_usuario>', views.updateUsuario, name="updateUsuario"),
    path('ver_usuario/<int:id_usuario>', views.verUsuario, name="verUsuario"),
    path('listar_usuarios/', views.listarUsuarios, name="listarUsuarios"),
    path('buscar_usuarios/', views.buscarUsuario, name="buscarUsuario"),
    path('crear_cuenta/<int:id_usuario>', views.crearCuenta, name="crearCuenta"),
]
