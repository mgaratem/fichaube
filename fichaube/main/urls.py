from django.contrib import admin
from django.urls import path
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


    # html's
    path('agregar-Area', areas.views.testpancho01, name="agregar-Area"),

    # controladores
    path('agregarArea', areas.views.agregarArea, name='agregarArea'),
    path('ajax/validarArea', areas.views.validarArea, name='validarArea'),
    path('lista-Areas', areas.views.listarArea, name="lista-Areas"),

]
