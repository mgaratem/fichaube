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
from django.db.models import Q

from alumnos.models import Alumno

# Create your views here.

#############---------FUNCION CREAR------#################

def crear_alumno(request):
    template = "crear_alumno.html"

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
            #ocupacion = request.POST.get('inputOcupacion')
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
                alumno.carrera = carrera.upper()
                alumno.domicilio = domicilio.upper()
                #alumno.ocupacion = ocupacion
                alumno.representante_legal = representante.upper()
                alumno.prevision = prevision.upper()

                alumno.save()
                messages.success(request, '¡Alumno agregado con éxito!')
                del alumno

            else:
                messages.error(request,'¡Este usuario ya existe!')
                del alumno
                return HttpResponseRedirect(reverse("alumnos:crear_alumno"))

        except Exception as e:
            messages.error(request,"No fue posible crear alumno. "+repr(e))
            del alumno
            return HttpResponseRedirect(reverse("alumnos:crear_alumno"))

        return HttpResponseRedirect(reverse("alumnos:crear_alumno"))




#############---------FUNCION BORRAR------#################

def borrarAlumno(request, id_alumno=None):

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id=id_alumno)
            alumno.delete()

            messages.success(request, '¡Alumno eliminado con éxito!')
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))

        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al alumno correctamente!')
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))




#############---------FUNCION MODIFICAR------#################

def updateAlumno(request, id_alumno=None): #Actualizar datos alumnos
    template = "actualizar_alumno.html"

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id = id_alumno)
            return render(request, template, {'alumno': alumno})

        except Exception as e:
            messages.error(request,"No fue posible modificar alumno. "+repr(e))
            return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))

    if request.method == 'POST':
        try:
            alumno = Alumno.objects.get(id = id_alumno)

            alumno.nombre = request.POST.get('inputNombre').upper()
            alumno.apellido_paterno = request.POST.get('inputApellidoPaterno').upper()
            alumno.apellido_materno = request.POST.get('inputApellidoMaterno').upper()
            #alumno.sexo = request.POST.get('inputSexo')
            alumno.correo = request.POST.get('inputCorreo')
            alumno.carrera = request.POST.get('inputCarrera')
            alumno.domicilio = request.POST.get('inputDomicilio')
            #alumno.ocupacion = request.POST.get('inputOcupacion')
            alumno.representante_legal = request.POST.get('inputRepresentante')
            alumno.prevision = request.POST.get('inputPrevision')

            alumno.save()
            messages.success(request, '¡Alumno modificado exitosamente!')
            return HttpResponseRedirect(reverse("alumnos:updateAlumno", args=[id_alumno]))
            #return verAlumno('get', id_alumno)

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
            return render(request, buscarAlumno)




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


#############---------FUNCION LISTAR------#################

def buscarAlumno(request):

    template = "buscar_alumno.html"
    if request.method == 'GET':
        return render(request, template)

    if request.method == "POST":
        try:
            filtro = request.POST.get('inputSearch')
            querys = (Q(nombre__icontains=filtro) | Q(apellido_materno__icontains=filtro))
            querys |= Q(apellido_paterno__icontains=filtro)
            querys |= Q(rut__icontains=filtro)

            alumnos = Alumno.objects.filter(querys)

            if not alumnos:
                messages.info(request,"No se encontró ningún alumno.")
                return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))
            else:
                return render(request, template, {'alumnos': alumnos})

        except Exception as e:
            messages.error(request,"No se pudo realizar la búsqueda. "+repr(e))
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))
