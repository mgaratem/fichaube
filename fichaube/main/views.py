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
from datetime import date, datetime
import logging
from django.urls import reverse
from django.template import *

# Create your views here.

#-----------------------------------------------------------FUNCIONES GENERALES!

#############---------FUNCION INDEX------#################

@login_required()
def index(request): #Home
    return render(request, 'home.html')



##############-----FUNCIONES HANDLERS 404 500-----####################

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)



#############---------FUNCION CREATE USER DJANGO------#################

def crearUser(request, nombre=None, apellido=None, email=None, rut=None):

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
        del user
        return True

    return False



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


# test de pancho
def testpancho(request):
    return render(request, 'testpancho.html',{})

def agregarArea(request):
    if request.method == 'POST':
        area = request.POST.get("area")
        
