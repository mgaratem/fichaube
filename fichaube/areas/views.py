from django.shortcuts import render
from areas.models import Area

# Create your views here.
# test de pancho
def testpancho(request):
    return render(request, 'testpancho.html',{})

def agregarArea(request):
    if request.method == 'POST':
        area = request.POST.get("area")
        nuevaArea = Area(nombreArea=area)
        nuevaArea.save()
