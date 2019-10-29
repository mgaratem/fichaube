import csv, io
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
from areas.models import Especialidad, Area, UsuarioEspecialidad
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *

# Create your views here.

#############---------FUNCION CREATE USER DJANGO------#################

def crear_user(request, nombre=None, apellido=None, email=None, rut=None):

    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN' #Evitar problemas letras especiales y tildes
    trans = str.maketrans(a,b)
    nombre_nuevo = nombre.translate(trans)
    apellido_nuevo = apellido.translate(trans)

    first_letra = nombre_nuevo[:1].lower()
    apellidoSplit = apellido_nuevo.split(" ")
    first_apellido = apellidoSplit[0].lower()
    second_apellido = apellidoSplit[1][:1].lower()

    primerNombre = nombre_nuevo.split(" ")[0]
    primerApellido =apellidoSplit[0]

    userName = first_letra + first_apellido + second_apellido
    userExiste = User.objects.filter(username=userName)
    if not userExiste:
        userPass = userName + '99'
        userEmail = email

        user = User.objects.create_user(username=userName,
                                        email=userEmail,
                                        password=userPass,
                                        first_name=primerNombre,
                                        last_name=primerApellido)
        user.save()
        return user

    return userExiste[0]



#############---------FUNCION CHANGE PASSWORD------#################

@login_required()
def cambiar_pass(request):
    template = "cambiar_pass.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:
            passVieja = request.POST.get('inputPassVieja')
            passNueva = request.POST.get('inputPassNueva')
            passConfirmacion = request.POST.get('inputPassConfirmada')

            user = authenticate(username=request.user.username, password=passVieja)

            if user is not None:
                if passNueva == passConfirmacion:
                    user.set_password(passNueva)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '¡Contraseña cambiada con éxito!')
                else:
                    messages.error(request,'Las contraseñas no coinciden')
                    return HttpResponseRedirect(reverse("cambiar_pass"))
            else:
                messages.error(request,'La contraseña no es la correcta')
                return HttpResponseRedirect(reverse("cambiar_pass"))

        except Exception as e:
            messages.error(request,"No es posible cambiar contraseña. "+repr(e))
            return HttpResponseRedirect(reverse("cambiar_pass"))

        return HttpResponseRedirect(reverse("cambiar_pass"))

    #return render(request, 'cambiar_pass.html')

#############---------FUNCION CREAR------#################

def crear_usuario(request):
    template = "crear_usuario.html"

    if request.method == 'GET':
        areas = Area.objects.all()
        especialidades = Especialidad.objects.all()
        return render(request, template, {"areas": areas, "especialidades": especialidades})

    if request.method == 'POST':
        try:

            nombre = request.POST.get('inputNombre')
            apellidos_paterno = request.POST.get('inputApellidoPaterno')
            apellidos_materno = request.POST.get('inputApellidoMaterno')
            txt_rut =  request.POST.get('inputRut')
            rut = txt_rut.replace(".", "")
            tipoUsuario = request.POST.get('inputTipoUsuario')
            correo = request.POST.get('inputCorreo')
            #FALTA AGREGAR ESPECIALIDADES
            usuarioExiste = Usuario.objects.filter(rut=rut)

            if not usuarioExiste:

                usuario = Usuario()
                usuario.nombre = nombre_alumno.upper()
                usuario.apellidos = apellidos_paterno.upper() + apellidos_materno.upper()
                usuario.rut = rut

                if tipoUsuario == 1:
                    usuario.coordinador = True
                elif tipoUsuario == 2:
                    usuario.profesional = True
                elif tipoUsuario == 3:
                    usuario.administrativo = True
                elif tipoUsuario == 4:
                    usuario.mantenedor = True
                else:
                    usuario.asistente_social = True

                usuario.user = crearUser('post', nombre, apellidos_paterno, correo)
                usuario.save()
                messages.success(request, '¡Usuario agregado con éxito!')
                del usuario
                return HttpResponseRedirect(reverse("crear_usuario"))

            else:
                messages.error(request,'¡Este usuario ya existe!')
                del usuario
                return HttpResponseRedirect(reverse("crear_usuario"))

        except Exception as e:
            messages.error(request,"No fue posible crear usuario. "+repr(e))
            del usuario
            return HttpResponseRedirect(reverse("crear_usuario"))




#############---------FUNCION BORRAR------#################

def borrarUsuario(request, id_usuario=None):

    if request.method == 'GET':
        try:
            user = User.objects.get(id=id_usuario)
            user.delete()

            messages.success(request, '¡Usuario eliminado con éxito!')
            return HttpResponseRedirect(reverse("listarUsuarios"))

        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al usuario correctamente!')
            return HttpResponseRedirect(reverse("listarUsuarios"))




#############---------FUNCION MODIFICAR------#################

def updateUsuario(request, id_usuario=None):
    template = "actualizar_usuario.html"

    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(id = id_usuario)
            return render(request, template, {'usuario': usuario})

        except Exception as e:
            messages.error(request,"No fue posible modificar usuario. "+repr(e))
            return HttpResponseRedirect(reverse("listarUsuarios"))

    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id = id_usuario)

            usuario.nombre = request.POST.get('inputNombre').upper()
            apellido_paterno = request.POST.get('inputApellidoPaterno')
            apellido_materno = request.POST.get('inputApellidoMaterno')
            usuario.apellidos = apellido_paterno.upper() + " " + apellido_materno.upper()
            tipoUsuario = request.POST.get('inputTipoUsuario')

            if tipoUsuario == 1:
                usuario.coordinador = True
                usuario.profesional = False
                usuario.administrativo = False
                usuario.mantenedor = False
                usuario.asistente_social = False
            elif tipoUsuario == 2:
                usuario.coordinador = False
                usuario.profesional = True
                usuario.administrativo = False
                usuario.mantenedor = False
                usuario.asistente_social = False
            elif tipoUsuario == 3:
                usuario.coordinador = False
                usuario.profesional = False
                usuario.administrativo = True
                usuario.mantenedor = False
                usuario.asistente_social = False
            elif tipoUsuario == 4:
                usuario.coordinador = False
                usuario.profesional = False
                usuario.administrativo = False
                usuario.mantenedor = True
                usuario.asistente_social = False
            else:
                usuario.coordinador = False
                usuario.profesional = False
                usuario.administrativo = False
                usuario.mantenedor = False
                usuario.asistente_social = True

            usuario.save()
            messages.success(request, '¡Usuario modificado exitosamente!')
            return HttpResponseRedirect(reverse("updateUsuario"))
            #return verUsuario('get', id_usuario)

        except Exception as e:
            messages.error(request,"No fue posible modificar usuario. "+repr(e))
            return verUsuario('get', id_usuario)





#############---------FUNCION MOSTRAR------#################

def verUsuario(request, id_usuario=None):

    template = "ver_usuario.html"
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(id = id_usuario)
            return render(request, template, {'usuario': usuario})

        except Exception as e:
            messages.error(request,"No fue posible mostrar usuario. "+repr(e))
            return render(request, listarUsuarios)




#############---------FUNCION LISTAR------#################

def listarUsuarios(request):

    template = "listar_usuarios.html"
    if request.method == 'GET':
        try:
            usuarios = Usuario.objects.all()
            return render(request, template, {'usuarios': usuarios})

        except Exception as e:
            messages.error(request,"No fue posible listar usuarios. "+repr(e))
            return render(request, "home.html")
