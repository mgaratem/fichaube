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
from django.contrib.auth.models import User
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *

from alumnos.models import Alumno

# Create your views here.

#############---------FUNCION CREAR------#################

def crear_alumno(request):
    template = "crear_usuario.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:

            nombre_alumno = request.POST.get('inputNombre')
            apellidos_paterno = request.POST.get('inputApellidoPaterno')
            apellidos_materno = request.POST.get('inputApellidoMaterno')
            txt_rut =  request.POST.get('inputRut')
            rut = txt_rut.replace(".", "")
            tipoDocumento = request.POST.get('inputTipoDocumento')
            fecha_nacimiento = request.POST.get('inputFechaNacimiento')
            sexo = request.POST.get('inputSexo')
            correo = request.POST.get('inputCorreo')
            carrera = request.POST.get('inputCarrera')
            domicilio = request.POST.get('inputDomicilio')
            ocupacion = request.POST.get('inputOcupacion')
            representante = request.POST.get('inputRepresentante')
            prevision = request.POST.get('inputPrevision')


            alumnoExiste = Alumno.objects.filter(rut=rut)

            if not alumnoExiste:

                alumno = Alumno()
                alumno.nombre = nombre_alumno.upper()
                alumno.apellido_paterno = apellidos_paterno.upper()
                alumno.apellido_materno = apellidos_materno.upper()
                alumno.rut = rut
                alumno.tipoDocumento = tipoDocumento
                alumno.fecha_nacimiento = fecha_nacimiento
                alumno.sexo = sexo
                alumno.correo = correo
                alumno.carrera = carrera
                alumno.domicilio = domicilio
                alumno.ocupacion = ocupacion
                alumno.representante_legal = representante
                alumno.prevision = prevision

                alumno.save()
                messages.success(request, '¡Alumno agregado con éxito!')
                del alumno

            else:
                messages.error(request,'¡Este usuario ya existe!')
                del alumno
                return HttpResponseRedirect(reverse("crear_alumno"))

        except Exception as e:
            messages.error(request,"No fue posible crear alumno. "+repr(e))
            del alumno
            return HttpResponseRedirect(reverse("crear_alumno"))

        return HttpResponseRedirect(reverse("crear_alumno"))




#############---------FUNCION BORRAR------#################

def borrarAlumno(request, id_alumno=None):

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id=id_alumno)
            alumno.delete()

            messages.success(request, '¡Alumno eliminado con éxito!')
            return HttpResponseRedirect(reverse("mechones"))

        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al alumno correctamente!')
            return HttpResponseRedirect(reverse("handler500"))




#############---------FUNCION MODIFICAR------#################

def updateAlumno(request, id_alumno=None): #Actualizar datos alumnos
    template = "actualizar_alumno.html"

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id = id_alumno)
            return render(request, template, {'alumno': alumno})

        except Exception as e:
            messages.error(request,"No fue posible modificar alumno. "+repr(e))
            return HttpResponseRedirect(reverse("listarAlumnos"))

    if request.method == 'POST':
        try:
            alumno = Alumno.objects.get(id = id_alumno)

            alumno.nombre = request.POST.get('inputNombre')
            alumno.apellido_paterno = request.POST.get('inputApellidoPaterno')
            alumno.apellido_materno = request.POST.get('inputApellidoMaterno')
            alumno.sexo = request.POST.get('inputSexo')
            alumno.correo = request.POST.get('inputCorreo')
            alumno.carrera = request.POST.get('inputCarrera')
            alumno.domicilio = request.POST.get('inputDomicilio')
            alumno.ocupacion = request.POST.get('inputOcupacion')
            alumno.representante = request.POST.get('inputRepresentante')
            alumno.prevision = request.POST.get('inputPrevision')

            alumno.save()
            return verAlumno('get', id_alumno)

        except Exception as e:
            messages.error(request,"No fue posible modificar alumno. "+repr(e))
            return verAlumno('get', id_alumno)





#############---------FUNCION MOSTRAR------#################

def verAlumno(request, id_alumno=None):

    template = "ver_alumno.html"
    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id = id_alumno)
            return render(request, template, {'alumno': alumno})

        except Exception as e:
            messages.error(request,"No fue posible mostrar alumno. "+repr(e))
            return render(request, listarAlumnos)




#############---------FUNCION LISTAR------#################

def listarAlumnos(request):

    template = "listar_alumnos.html"
    if request.method == 'GET':
        try:
            alumnos = Alumno.objects.all()
            return render(request, template, {'alumnos': alumnos})

        except Exception as e:
            messages.error(request,"No fue posible listar alumnos. "+repr(e))
            return render(request, "home.html")
