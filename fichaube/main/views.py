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
from datetime import date, datetime, time
import logging
from django.urls import reverse
from django.template import *
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from usuarios.models import Usuario

# Create your views here.

#-----------------------------------------------------------FUNCIONES GENERALES!

#############---------FUNCION INDEX (HOME)------#################

@login_required()
def index(request):

    user = request.user
    if user.is_superuser:
        return render(request, 'home.html')

    usuario = Usuario.objects.get(user=user)

    #date_joined = datetime.combine(user.date_joined.date(), time(user.date_joined.hour, user.date_joined.minute))
    #last_login = datetime.combine(user.last_login.date(), time(user.last_login.hour, user.last_login.minute))
    #print (last_login)
    #print(date_joined)

    if usuario.has_previously_logged_in:
        return render(request, 'home.html')
    else:
        messages.warning(request, 'Por seguridad, por favor cambie su contraseña.')
        return HttpResponseRedirect(reverse("force_cambiar_pass"))



##############-----FUNCIONES HANDLERS 404 500-----####################

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


##############---------FUNCION DE CAMBIO PASSWORD----------####################


@login_required()
def force_cambiar_pass(request):
    template = "force_cambiar_pass.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(user=request.user)
            passVieja = usuario.rut.split("-")[0][-4:]
            passNueva = request.POST.get('inputPassNueva')
            passConfirmacion = request.POST.get('inputPassConfirmada')
            print(passVieja, passNueva, passConfirmacion)
            user = authenticate(username=request.user.username, password=passVieja)

            if user is not None:
                if passNueva == passConfirmacion:
                    user.set_password(passNueva)
                    user.save()
                    update_session_auth_hash(request, user)
                    usuario.has_previously_logged_in = True
                    usuario.save()
                    print(usuario.nombre)
                    messages.success(request, '¡Contraseña cambiada con éxito!')
                else:
                    messages.error(request,'Las contraseñas no coinciden')
                    return HttpResponseRedirect(reverse("force_cambiar_pass"))
            else:
                messages.error(request,'La contraseña no es la correcta')
                return HttpResponseRedirect(reverse("force_cambiar_pass"))

        except Exception as e:
            messages.error(request,"No es posible cambiar contraseña. "+repr(e))
            return HttpResponseRedirect(reverse("force_cambiar_pass"))

        return HttpResponseRedirect(reverse("home"))
