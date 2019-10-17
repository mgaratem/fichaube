from django.db import models


# Create your models here.

########### CLASE AREA #########################

class Area(models.Model):
  nombreArea = models.CharField(max_length = 255)
  def __str__(self):
      return self.nombreArea

########### CLASE ESPECIALIDAD #########################

class Especialidad(models.Model):
  nombreEspecialidad = models.CharField(max_length = 255)
  area = models.ForeignKey(Area, on_delete = models.SET_NULL)
  def __str__(self):
      return self.nombreEspecialidad
