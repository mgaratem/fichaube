from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

########### CLASE USUARIO #########################

class Usuario(models.Model):

  nombre = models.CharField(max_length = 50, null=False)
  apellidos = models.CharField(max_length = 50, null=False)
  rut = models.CharField(max_length = 40, unique=True, null=False)
  coordinador = models.BooleanField(default=False, null=False)
  profesional = models.BooleanField(default=False, null=False)
  administrativo = models.BooleanField(default=False, null=False)
  mantenedor = models.BooleanField(default=False, null=False)
  asistente_social = models.BooleanField(default=False, null=False)

  user = models.OneToOneField(User, null=True, on_delete = models.SET_NULL) #USUARIO DJANGO

  def get_nombre(self):
      return self.nombre + " " + self.apellidos

  def __str__(self):
      return 'Rut={0}, Nombre={1}, Apellido={2}, Rut{3}, Coordinador{4}, Profesional{5}, Administrador{6}, Mantenedor{7}, Asistente{8}'.format(self.rut, self.nombre, self.apellidos, self.rut, self.coordinador, self.profesional, self.administrativo, self.mantenedor, self.asistente_social)
