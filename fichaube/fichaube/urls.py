"""fichaube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('areas/', include('areas.urls')),
    path('fichaube/', include('main.urls')),
    path('coordinador/', include('coordinador.urls')),
    path('profesional/', include('profesional.urls')),
    path('administrativo/', include('administrativo.urls')),
    path('mantenedor/', include('mantenedor.urls')),
    path('alumnos/', include('alumnos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('fichas/', include('fichas.urls')),
    path('permisos/', include('permisos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
