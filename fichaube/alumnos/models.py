from django.db import models
from datetime import date, datetime

# Create your models here.

########### CLASE ALUMNO #########################

class Alumno(models.Model):

  nombre = models.CharField(max_length = 50, null=False)
  apellido_paterno = models.CharField(max_length = 50, null=False)
  apellido_materno = models.CharField(max_length = 50, null=False)
  rut = models.CharField(max_length = 40, unique=True, null=False)
  tipoDocumento = models.CharField(max_length = 40, null=False)
  fecha_nacimiento = models.DateField(blank=True, null=True)
  sexo = models.CharField(max_length = 30, blank=True)
  correo = models.EmailField(max_length=250)
  carrera = models.CharField(max_length=120)
  domicilio = models.CharField(max_length=150, blank=True)
  ocupacion = models.CharField(max_length=100, default='Estudiante')
  representante_legal = models.CharField(max_length=100, blank=True, null=True)
  prevision = models.CharField(max_length=100, blank=True)
  nombre_social = models.CharField(max_length=100, null=True, default='-')

  def get_name(self):
      return self.nombre + " " + self.apellido_paterno + " " + self.apellido_materno

  def __str__(self):
    return 'Rut={0}, Nombre={1}, ApellidoPaterno={2}, ApellidoMaterno={3}, Carrera={4}, Domicilio={5}, Ocupacion={6}, Representante={7}, Prevision={8}'.format(self.rut, self.nombre, self.apellido_paterno, self.apellido_materno, self.carrera, self.domicilio, self.ocupacion, self.representante_legal, self.prevision)

  def get_fecha(self):
      if self.fecha_nacimiento:
          return self.fecha_nacimiento.strftime('%d/%m/%Y')
      else:
          return False


class Carrera(models.Model):
    nombre_carrera = models.CharField(max_length=120, null=False)


class Prevision(models.Model):
    nombre_prevision = models.CharField(max_length=120, null=False)
