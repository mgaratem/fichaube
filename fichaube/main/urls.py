from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # HANDLERS
    path('404/', views.handler404, name="404"),
    path('500/', views.handler500, name="500"),
    path('testarea', views.testpancho, name="nameTestpancho"),
    path('agregarArea', views.agregarArea, name='agregarArea'),
]
