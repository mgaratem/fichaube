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

from django.contrib.auth.models import User
from alumnos.models import Alumno

# Create your views here.


#############---------FUNCION CREAR------#################

@login_required()
def crearFicha(request, id_alumno):
    template = "crear_ficha.html"

    if request.method == 'GET':
        try:
            alumno = Alumno.object.get(id=id_alumno)

            ficha = Ficha()
            ficha.alumno =
        return render(request, template)

    if request.method == 'POST':
        try:
            alumno = Alumno.object.get(id=id_alumno)

            ficha = Ficha()
            ficha.alumno =


#############---------FUNCION BORRAR------#################

@login_required()
def borrarFicha(request):


#############---------FUNCION MODIFICAR------#################

@login_required()
def updateFicha(request):


#############---------FUNCION MOSTRAR------#################

@login_required()
def verFicha(request):


#############---------FUNCION LISTAR------#################

@login_required()
def listarFichas(request):


#############---------FUNCION BUSCAR------#################

@login_required()
def buscarFicha(request):
