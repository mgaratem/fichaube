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
                alumno.apellidos = apellidos_alumno.upper()
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

def borrar_alumno(request, id_alumno=None): #Elimina alumno completamente, junto con user y actividad

    tipoAlumno = None

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id=id_alumno)
            tipoAlumno = alumno.es_Mechon
            id_usuario = alumno.usuario_id
            user = User.objects.get(id=id_usuario)
            user.delete()
            alumno.delete()

            if tipoAlumno:
                messages.success(request, '¡Alumno eliminado con éxito!')
                return HttpResponseRedirect(reverse("mechones"))
            else:
                messages.success(request, '¡Alumno eliminado con éxito!')
                return HttpResponseRedirect(reverse("padrinos"))

        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al alumno correctamente!')
            return HttpResponseRedirect(reverse("handler500"))



#############---------FUNCION MODIFICAR------#################

def updateAlumno(request): #Actualizar datos alumnos
    template = "crear_encuesta.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':

    return redirect()
