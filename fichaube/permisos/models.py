from django.db import models
from usuarios.models import Usuario
from fichas.models import Ficha

# Create your models here.

########### CLASE PERMISOS #########################

class Permiso(models.Model):
  usuario =  models.ForeignKey(Usuario, on_delete = models.CASCADE)
  ficha = models.ForeignKey(Ficha, on_delete = models.CASCADE)

  def get_nombre(self):
      return self.usuario.nombre + " " + self.usuario.apellidos
