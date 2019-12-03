from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from areas.models import Area
from areas.models import Especialidad
from django.http import JsonResponse

# Create your views here.



# html para agregar area
def testpancho01(request):
    return render(request, 'agregar-Area.html',{})

# html para editar area
def testpancho02(request, idArea):
    area = Area.objects.get(pk = idArea)
    nombreArea = area.nombreArea
    return render(request, 'editar-Area.html', {'idArea': idArea, 'nombreArea': nombreArea})

# html para agregar especialidad
def testpancho03(request, idArea):
    return HttpResponseRedirect(reverse(request, 'agregar-Especialidad.html', {'idArea': idArea}))




# funcion para agregar areas
def agregarArea(request):
    if request.method == 'POST':
        area = request.POST.get("area")
        nuevaArea = Area(nombreArea=area)
        nuevaArea.save()
        del nuevaArea
        return HttpResponseRedirect(reverse('lista-Areas'))

# funcion para corroborar si el area ya existe
def validarArea(request):
    area = request.GET.get('area', None)
    data = {
        'is_taken': Area.objects.filter(nombreArea=area).exists()
        #'is_taken': True
    }
    return JsonResponse(data)

# funcion y html para listar Areas
def listarAreas(request):
    listaAreas = Area.objects.all()
    return render(request, 'lista-Areas.html', {"areas": listaAreas})

# funcion para eliminar una Area dado un ID
def eliminarArea(request, idArea):
    # idArea = request.GET.get("idArea")
    Area.objects.filter(id=idArea).delete()
    return HttpResponseRedirect(reverse('lista-Areas'))
#******************FALTA eliminar en cascada


def editarArea(request):
    if request.method == 'POST':
        idArea = request.POST.get("idArea")
        nuevoNombreArea = request.POST.get("nuevoNombreArea")
        area = Area.objects.get(pk=idArea)
        area.nombreArea = nuevoNombreArea
        area.save()
        return HttpResponseRedirect(reverse('lista-Areas'))



def listarEspecialidades(request, idArea):
    listaEspecialides = Especialidad.objects.filter(area_id = idArea)
    return render(request, 'lista-Especialidades.html', {"especialidades": listaEspecialides})

def agregarEspecialidad(request):
    return True
