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
from django.contrib.auth.models import User, Group
from areas.models import Especialidad, Area, UsuarioEspecialidad
from usuarios.models import Usuario
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *
from django.db.models import Q
from django.core.mail import send_mail

# Create your views here.

#############---------FUNCION CREATE USER DJANGO------#################

def crear_user(nombre=None, apellido=None, email=None, tipoUsuario=None, cedula=None):

    try:
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

            #password = User.objects.make_random_password()
            rut = cedula.split("-")
            password = rut[0][-4:]

            userEmail = email

            user = User.objects.create_user(username=userName,
                                            email=userEmail,
                                            password=password,
                                            first_name=primerNombre,
                                            last_name=primerApellido)
            user.save()

            if tipoUsuario == "1":
                #PROFESIONAL
                group = Group.objects.get(name='Profesional')
                group.user_set.add(user)

            elif tipoUsuario == "2":
                #ADMINISTRATIVO
                group = Group.objects.get(name='Administrativo')
                group.user_set.add(user)

            elif tipoUsuario == "3":
                #MANTENEDOR
                group = Group.objects.get(name='Mantenedor')
                group.user_set.add(user)

            elif tipoUsuario == "4":
                #ASISTENTE SOCIAL
                group = Group.objects.get(name='Asistente Social')
                group.user_set.add(user)

            elif tipoUsuario == "5":
                #COORDINADOR
                group = Group.objects.get(name='Coordinador')
                group.user_set.add(user)


                send_mail(
                    'Password FichaUbe',
                    'Acá tiene su contraseña de su cuenta en FichaUbe: ' + password,
                    'from@example.com',
                    ['to@example.com'],
                    fail_silently=False,
                )

            return user

        return userExiste[0]

    except Exception as e:
        messages.error(request,"No fue posible crear usuario. "+repr(e))
        return HttpResponseRedirect(reverse("usuarios:crear_usuario"))



#############---------FUNCION CREAR UN USUARIO PARA PROFESIONAL------#################

@login_required()
def crearCuenta(request, id_usuario=None):

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
                usuario = Usuario.objects.get(id = id_usuario)
                if usuario.user:
                    messages.error(request,"Este usuario ya tiene cuenta.")
                    return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))

                correo = "example@example.com"

                tipoUsuario = ""
                if usuario.profesional == True:
                    tipoUsuario = "1"
                elif usuario.administrativo == True:
                    tipoUsuario = "2"
                elif usuario.mantenedor == True:
                    tipoUsuario = "3"
                elif usuario.asistente_social == True:
                    tipoUsuario = "4"
                elif usuario.coordinador == True:
                    tipoUsuario = "5"

                usuario.user = crear_user(usuario.nombre, usuario.apellidos, correo, tipoUsuario, usuario.rut)
                usuario.save()
                messages.success(request, '¡Cuenta creada con éxito!')
                return HttpResponseRedirect(reverse("usuarios:verUsuario", args=[id_usuario]))

            except Exception as e:
                messages.error(request,"No fue posible crear user para usuario. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))



#############---------FUNCION CHANGE PASSWORD------#################

@login_required()
def cambiarPass(request):
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
                    return HttpResponseRedirect(reverse("usuarios:cambiarPass"))
            else:
                messages.error(request,'La contraseña no es la correcta')
                return HttpResponseRedirect(reverse("usuarios:cambiarPass"))

        except Exception as e:
            messages.error(request,"No es posible cambiar contraseña. "+repr(e))
            return HttpResponseRedirect(reverse("usuarios:cambiarPass"))

        return HttpResponseRedirect(reverse("usuarios:cambiarPass"))

    #return render(request, 'cambiar_pass.html')

#############---------FUNCION CREAR------#################

@login_required()
def crear_usuario(request):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "crear_usuario.html"

        if request.method == 'GET':
            areas = Area.objects.all()
            especialidades = Especialidad.objects.all()
            return render(request, template, {"areas": areas, "especialidades": especialidades})

        if request.method == 'POST':
            try:

                nombre = request.POST.get('inputNombre').upper()
                apellido_paterno = request.POST.get('inputApellidoPaterno').upper()
                apellido_materno = request.POST.get('inputApellidoMaterno').upper()
                txt_rut =  request.POST.get('inputRut')
                rut = txt_rut.replace(".", "")
                tipoUsuario = request.POST.get('inputTipoUsuario')
                correo = request.POST.get('inputCorreo')
                especialidadesElegidas = request.POST.getlist('inputEspecialidad')
                apellidos =  apellido_paterno.upper() + " " + apellido_materno.upper()
                #print (especialidadesElegidas)

                usuarioExiste = Usuario.objects.filter(rut=rut)

                if not usuarioExiste:

                    usuario = Usuario()
                    usuario.nombre = nombre.upper()
                    usuario.apellidos = apellidos
                    usuario.rut = rut

                    if tipoUsuario == "1":
                        usuario.profesional = True
                    elif tipoUsuario == "2":
                        usuario.administrativo = True
                    elif tipoUsuario == "3":
                        usuario.mantenedor = True
                    elif tipoUsuario == "4":
                        usuario.asistente_social = True
                    elif tipoUsuario == "5":
                        usuario.coordinador = True

                    usuario.user = crear_user(nombre, apellidos, correo, tipoUsuario, rut)
                    usuario.save()

                    if especialidadesElegidas:
                        for e in especialidadesElegidas:
                            obj = UsuarioEspecialidad()
                            especialidad = Especialidad.objects.get(id=e)
                            obj.especialidad = especialidad
                            obj.usuario = usuario
                            obj.save()


                    messages.success(request, '¡Usuario agregado con éxito!')
                    id = usuario.id
                    del usuario
                    return HttpResponseRedirect(reverse("usuarios:verUsuario", args=[id] ))

                else:
                    usuario = usuarioExiste[0]
                    usuario.user = crear_user(nombre, apellidos, correo, tipoUsuario, rut)
                    messages.error(request,'¡Este usuario ya existe!')
                    return HttpResponseRedirect(reverse("usuarios:crear_usuario"))

            except Exception as e:
                messages.error(request,"No fue posible crear usuario. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:crear_usuario"))




#############---------FUNCION BORRAR------#################

@login_required()
def borrarUsuario(request, id_usuario=None):

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
                usuario = Usuario.objects.get(id=id_usuario)
                usuario.has_previously_logged_in = False
                usuario.save()
                user = User.objects.get(id=usuario.user_id)
                user.delete()
                messages.success(request, '¡Usuario eliminado con éxito!')
                return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))

            except ObjectDoesNotExist:
                messages.error(request,'ERROR - ¡No se pudo eliminar al usuario correctamente!')
                return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))




#############---------FUNCION MODIFICAR------#################

@login_required()
def updateUsuario(request, id_usuario=None):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "actualizar_usuario.html"
        areas = Area.objects.all()
        especialidades = Especialidad.objects.all()
        usuario = Usuario.objects.get(id = id_usuario)
        userEsp = UsuarioEspecialidad.objects.filter(usuario = usuario)

        if request.method == 'GET':
            try:
                return render(request, template, {'usuario': usuario, 'areas': areas, 'especialidades': especialidades, 'usuarioEspecialidades': userEsp})

            except Exception as e:
                messages.error(request,"No fue posible modificar usuario. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:verUsuario", args=[id_usuario]))

        if request.method == 'POST':
            try:

                especialidadesElegidas = request.POST.getlist('inputEspecialidad')
                correo = request.POST.get('inputCorreo')
                activado = request.POST.get('inputDesactivar')

                if especialidadesElegidas:

                    #SI SE AGREGA NUEVA ESPECIALIDAD
                    for e in especialidadesElegidas:
                        query1 =  userEsp.filter(especialidad=e)
                        if not query1:
                            obj = UsuarioEspecialidad()
                            especialidad = Especialidad.objects.get(id=e)
                            obj.especialidad = especialidad
                            obj.usuario = usuario
                            obj.save()

                    #SI SE QUITA UNA ESPECIALIDAD
                    query2 = UsuarioEspecialidad.objects.filter(usuario = usuario)
                    for e in especialidadesElegidas:
                        query2 = query2.exclude(especialidad=e)

                    for esp in query2:
                        esp.delete()

                user = User.objects.filter(id=usuario.user_id)

                if user:
                    user[0].email = correo

                    if activado == "1":
                        user[0].is_active = True
                    else:
                        user[0].is_active = False

                    user[0].save()

                #usuario.save()
                messages.success(request, '¡Usuario modificado exitosamente!')
                return HttpResponseRedirect(reverse("usuarios:verUsuario", args=[id_usuario]))
                #return verUsuario('get', id_usuario)

            except Exception as e:
                messages.error(request,"No fue posible modificar usuario. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:verUsuario", args=[id_usuario]))





#############---------FUNCION MOSTRAR------#################

@login_required()
def verUsuario(request, id_usuario=None):
    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "ver_usuario.html"
        if request.method == 'GET':
            try:
                especialidadesUsuario = UsuarioEspecialidad.objects.filter(usuario_id = id_usuario)
                usuario = Usuario.objects.get(id = id_usuario)
                return render(request, template, {'usuario': usuario, 'especialidades': especialidadesUsuario})

            except Exception as e:
                messages.error(request,"No fue posible mostrar usuario. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))




#############---------FUNCION LISTAR------#################

@login_required()
def listarUsuarios(request):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "listar_profesionales.html"
        if request.method == 'GET':
            try:
                usuarios = Usuario.objects.filter(tipoUsuario )
                return render(request, template, {'usuarios': usuarios})

            except Exception as e:
                messages.error(request,"No fue posible listar usuarios. "+repr(e))
                return render(request, "home.html")



#############---------FUNCION BUSCAR------#################

@login_required()
def buscarUsuario(request):

    #PERMISOS
    if request.user.groups.filter(name__in=['Mantenedor']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Profesional']).exists():
        return HttpResponseRedirect(reverse("home"))
    elif request.user.groups.filter(name__in=['Asistente Social']).exists():
        return HttpResponseRedirect(reverse("home"))
    else:

        template = "buscar_usuario.html"
        if request.method == 'GET':
            return render(request, template)

        if request.method == "POST":
            try:
                filtro = request.POST.get('inputSearch')
                querys = (Q(nombre__icontains=filtro) | Q(apellidos__icontains=filtro))
                querys |= Q(rut__icontains=filtro)

                usuarios = Usuario.objects.filter(querys)

                if not usuarios:
                    messages.info(request,"No se encontró ningún usuario.")
                    return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))
                else:
                    return render(request, template, {'usuarios': usuarios})

            except Exception as e:
                messages.error(request,"No se pudo realizar la búsqueda. "+repr(e))
                return HttpResponseRedirect(reverse("usuarios:buscarUsuario"))
