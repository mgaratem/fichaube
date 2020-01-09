from django.db import models
from alumnos.models import Alumno
from usuarios.models import Usuario
import datetime
from datetime import date, datetime
import random
from random import seed, randint

# Create your models here.

########### CLASE FICHA #########################

class Ficha(models.Model):

    def number():
        numero =  int(date.today().year) * 100000 +  Ficha.objects.count()
        return numero + 1

    numero_folio = models.BigIntegerField(default=number, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    alumno = models.OneToOneField(Alumno, null=True, on_delete=models.PROTECT)


    def get_fecha(self):
        return self.fecha_creacion.strftime('%d/%m/%Y')

    def __str__(self):
        return 'Alumno={0}, Fecha={1}'.format(self.alumno, self.fecha_creacion)



########### CLASE REGISTRO #########################

class Registro(models.Model):

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    motivo_atencion = models.CharField(max_length = 50, null=False) # tambien es especialidad del profesional
    descripcion_atencion = models.TextField()
    es_asistencia_social = models.BooleanField(default=False, null=False)

    profesional = models.ForeignKey(Usuario, on_delete = models.PROTECT)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)

    def get_fecha(self):
        return self.fecha_creacion.strftime('%d/%m/%Y')
