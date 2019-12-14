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
from django.contrib.auth.models import User, Group
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *
from django.db.models import Q
import csv
import codecs
import re

from alumnos.models import Alumno
from usuarios.models import Usuario
from fichas.models import Ficha
from permisos.models import Permiso

# Create your views here.

#############---------FUNCION CREAR------#################

@login_required()
def cederPermiso(request, id_alumno=None):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "ceder_permiso.html"

        if request.method == 'GET':
            ficha = Ficha.objects.get(alumno_id = id_alumno)
            querys = (Q( profesional= True) | Q(asistente_social = True))
            profesionales = Usuario.objects.filter(querys)
            profesionalesSinPermiso = profesionales.exclude(permiso__ficha__id = ficha.id)
            return render(request, template, {'usuarios': profesionalesSinPermiso, 'ficha':ficha})

        if request.method == 'POST':
            try:
                rutUsuario = request.POST.get('inputRutProfesional')
                print(rutUsuario)
                print(id_alumno)
                if rutUsuario:
                    permiso = Permiso()
                    permiso.ficha = Ficha.objects.get(alumno_id = id_alumno)
                    permiso.usuario = Usuario.objects.get(rut = rutUsuario)
                    permiso.save()
                    del permiso

                    messages.success(request, '¡Permiso cedido con éxito!')
                    return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))

                messages.error(request,'¡No se elegió usuario!')
                return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))

            except Exception as e:
                messages.error(request,'¡No se pudo ceder permisos al usuario!')
                return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))




#############---------FUNCION BORRAR------#################

@login_required()
def revocarPermiso(request, id_permiso=None, id_alumno=None):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        if request.method == 'GET':
            try:
                permiso = Permiso.objects.get(id = id_permiso)
                permiso.delete()
                del permiso

                messages.success(request, '¡Permiso revocado con éxito!')
                return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))

            except ObjectDoesNotExist:
                messages.error(request,'ERROR - ¡No se pudo revocar el permiso correctamente!')
                return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))
