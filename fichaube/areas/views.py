from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from areas.models import Area
from django.http import JsonResponse

# Create your views here.



# html para agregar area
def testpancho01(request):
    return render(request, 'agregar-Area.html',{})

# html para editar area
def testpancho02(request, idArea):
    area = Area.objects.get(pk=idArea)
    nombreArea = area.nombreArea
    return render(request, 'editar-Area.html', {'idArea': idArea, 'nombreArea': nombreArea})






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
def listarArea(request):
    listaAreas = Area.objects.all()
    return render(request, 'lista-Areas.html', {"areas": listaAreas})



# funcion para eliminar una Area dado un ID
def eliminarArea(request, idArea):
    # idArea = request.GET.get("idArea")
    Area.objects.filter(id=idArea).delete()
    return HttpResponseRedirect(reverse('lista-Areas'))



def editarArea(request):
    return HttpResponseRedirect(reverse('lista-Areas'))
