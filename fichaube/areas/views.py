from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from datetime import date, datetime
import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from areas.models import Area
from areas.models import Especialidad
from django.http import JsonResponse
from django.template import *


# Create your views here.



# html para agregar area
@login_required()
def testpancho01(request):
    return render(request, 'agregar_Area.html',{})

# html para editar area
@login_required()
def testpancho02(request, idArea):
    area = Area.objects.get(pk = idArea)
    nombreArea = area.nombreArea
    return render(request, 'editar_Area.html', {'idArea': idArea, 'nombreArea': nombreArea})

# html para agregar especialidad
@login_required()
def testpancho03(request):
    if request.method == 'POST':
        idArea = request.POST.get("idArea")
        area = Area.objects.get(pk = idArea)
        nombreArea = area.nombreArea
        return render(request, 'agregar_Especialidad.html', {'idArea': idArea, 'nombreArea': nombreArea})

# html para editar una especialidad
@login_required()
def testpancho04(request, idEspecialidad, idArea):
    especialidad = Especialidad.objects.get(pk = idEspecialidad)
    nombreEspecialidad = especialidad.nombreEspecialidad
    return render(request, 'editar_Especialidad.html',{'idArea': idArea, 'nombreEspecialidad': nombreEspecialidad, 'idEspecialidad': idEspecialidad})




# funcion para agregar areas
@login_required()
def agregarArea(request):
    if request.method == 'POST':
        area = request.POST.get("area")
        nuevaArea = Area(nombreArea=area)
        nuevaArea.save()
        del nuevaArea
        return redirect('areas:lista_Areas')

# funcion para corroborar si el area ya existe, se utiliza via AJAX
@login_required()
def validarArea(request):
    area = request.GET.get('area', None)
    data = {
        'is_taken': Area.objects.filter(nombreArea=area).exists()
    }
    return JsonResponse(data)

# funcion y html para listar Areas
@login_required()
def listarAreas(request):
    listaAreas = Area.objects.all()
    return render(request, "lista_Areas.html", {"areas": listaAreas})

# funcion para eliminar una Area dado un ID
@login_required()
def eliminarArea(request, idArea):
    # idArea = request.GET.get("idArea")
    Area.objects.filter(id=idArea).delete()
    return HttpResponseRedirect(reverse("areas:lista_Areas"))


# funcion para editar el nombre de un area
@login_required()
def editarArea(request):
    if request.method == 'POST':
        idArea = request.POST.get("idArea")
        nuevoNombreArea = request.POST.get("nuevoNombreArea")
        area = Area.objects.get(pk=idArea)
        area.nombreArea = nuevoNombreArea
        area.save()
        return HttpResponseRedirect(reverse("areas:lista_Areas"))



# funcion para listar todas las especialidades
@login_required()
def listarEspecialidades(request, idArea):
    listaEspecialides = Especialidad.objects.filter(area_id = idArea)
    return render(request, "lista_Especialidades.html", {"especialidades": listaEspecialides, "idArea": idArea})

# funcion para agregar una nueva especialidad
@login_required()
def agregarEspecialidad(request):
    if request.method == 'POST':
        idArea = request.POST.get("idArea")
        area = Area.objects.get(pk=idArea)
        especialidad = request.POST.get("especialidad")
        nuevaEspecialidad = Especialidad(nombreEspecialidad=especialidad)
        nuevaEspecialidad.area = area
        nuevaEspecialidad.save()
        del nuevaEspecialidad
        direccion = "lista_Especialidades/" + idArea
        return redirect(direccion)
    return True

# funcion para corroborar si la especialidad ya existe, se utiliza via AJAX
@login_required()
def validarEspecialidad(request):
    especialidad = request.GET.get('especialidad', None)
    data = {
        'is_taken': Especialidad.objects.filter(nombreEspecialidad=especialidad).exists()
    }
    return JsonResponse(data)

# funcion para eliminar una Especialidad dado un ID
@login_required()
def eliminarEspecialidad(request, idEspecialidad, idArea):
    Especialidad.objects.filter(id=idEspecialidad).delete()
    direccion = "/areas/lista_Especialidades/" + str(idArea)
    return redirect(direccion)

# funcion para editar el nombre de una especialidad
@login_required()
def editarEspecialidad(request):
    if request.method == 'POST':
        idArea = request.POST.get("idArea")
        nuevoNombreEspecialidad = request.POST.get("nuevoNombreEspecialidad")
        idEspecialidad = request.POST.get("idEspecialidad")
        especialidad = Especialidad.objects.get(pk=idEspecialidad)
        especialidad.nombreEspecialidad = nuevoNombreEspecialidad
        especialidad.save()
        direccion = "/areas/lista_Especialidades/" + str(idArea)
        return redirect(direccion)
