from django.shortcuts import render

# Create your views here.
# test de pancho
def testpancho(request):
    return render(request, 'testpancho.html',{})

def agregarArea(request):
    if request.method == 'POST':
        area = request.POST.get("area")
