from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from areas.models import Area

# Create your views here.


# test de pancho

# html para agregar area
def testpancho01(request):
    return render(request, 'agregar-Area.html',{})




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
        'is_taken': User.objects.filter(area__iexact=area).exists()
    }
    return JsonResponse(data)


# funcion y html para listar Areas
def listarArea(request):
    listaAreas = Area.objects.all()
    return render(request, 'lista-Areas.html', {"areas": listaAreas})
