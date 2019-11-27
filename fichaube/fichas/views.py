from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *
from django.db.models import Q

from django.contrib.auth.models import User
from alumnos.models import Alumno
from fichas.models import Ficha
from fichas.models import Registro

# Create your views here.


#############---------FUNCION CREAR------#################

@login_required()
def crearFicha(request, id_alumno=None):
    template = "crear_ficha.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == "POST":
        try:
            alumnos_sin_ficha = Alumno.objects.filter(ficha__alumno__isnull=True)#.values_list('id', 'nombre', 'apellido_paterno', 'apellido_materno', 'rut')
            #print(alumnos.query)
            filtro = request.POST.get('inputSearch')
            querys = (Q(nombre__icontains=filtro) | Q(apellido_materno__icontains=filtro))
            querys |= Q(apellido_paterno__icontains=filtro)
            querys |= Q(rut__icontains=filtro)
            alumnos = alumnos_sin_ficha.filter(querys)
            return render(request, template, {'alumnos': alumnos})

        except Exception as e:
            messages.error(request,"No fue posible encontrar alumnos sin fichas clínicas. "+repr(e))
            return render(request, "home.html")


#############---------FUNCION BORRAR------#################

#@login_required()
#def borrarFicha(request):

#############---------FUNCION MODIFICAR------#################

#@login_required()
#def updateFicha(request):


#############---------FUNCION MOSTRAR------#################

#@login_required()
#def verFicha(request):


#############---------FUNCION LISTAR------#################

#@login_required()
#def listarFichas(request):


#############---------FUNCION BUSCAR------#################

#@login_required()
#def buscarFicha(request):
