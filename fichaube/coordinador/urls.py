from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'coordinador'

urlpatterns = [
    path('home/', views.index, name='home'),
    path('usuarios/', include('usuarios.urls')),
]
