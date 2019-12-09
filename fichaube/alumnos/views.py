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
from django.db.models import Q
import csv
import codecs
import re

from alumnos.models import Alumno
from fichas.models import Ficha, Registro

# Create your views here.

#############---------FUNCION CREAR------#################

@login_required()
def crear_alumno(request):
    template = "crear_alumno.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:

            nombre_alumno = request.POST.get('inputNombre')
            apellidos_paterno = request.POST.get('inputApellidoPaterno')
            apellidos_materno = request.POST.get('inputApellidoMaterno')
            txt_rut =  request.POST.get('inputRut')
            rut = txt_rut.replace(".", "")
            tipoDocumento = request.POST.get('inputTipoDocumento')
            fecha_nacimiento = request.POST.get('inputFechaNacimiento')
            sexo = request.POST.get('inputSexo')
            correo = request.POST.get('inputCorreo')
            carrera = request.POST.get('inputCarrera')
            domicilio = request.POST.get('inputDomicilio')
            #ocupacion = request.POST.get('inputOcupacion')
            representante = request.POST.get('inputRepresentante')
            prevision = request.POST.get('inputPrevision')


            alumnoExiste = Alumno.objects.filter(rut=rut)

            if not alumnoExiste:

                alumno = Alumno()
                alumno.nombre = nombre_alumno.upper()
                alumno.apellido_paterno = apellidos_paterno.upper()
                alumno.apellido_materno = apellidos_materno.upper()
                alumno.rut = rut
                alumno.tipoDocumento = tipoDocumento
                alumno.fecha_nacimiento = fecha_nacimiento
                alumno.sexo = sexo
                alumno.correo = correo
                alumno.carrera = carrera.upper()
                alumno.domicilio = domicilio.upper()
                #alumno.ocupacion = ocupacion
                alumno.representante_legal = representante.upper()
                alumno.prevision = prevision.upper()

                alumno.save()
                id = alumno.id
                del alumno
                messages.success(request, '¡Alumno agregado con éxito!')
                return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id]))

            else:
                messages.error(request,'¡Este usuario ya existe!')
                del alumno
                return HttpResponseRedirect(reverse("alumnos:crear_alumno"))

        except Exception as e:
            messages.error(request,"No fue posible crear alumno. "+repr(e))
            del alumno
            return HttpResponseRedirect(reverse("alumnos:crear_alumno"))

        return HttpResponseRedirect(reverse("alumnos:crear_alumno"))




#############---------FUNCION BORRAR------#################

@login_required()
def borrarAlumno(request, id_alumno=None):

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id=id_alumno)
            alumno.delete()

            messages.success(request, '¡Alumno eliminado con éxito!')
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))

        except ObjectDoesNotExist:
            messages.error(request,'ERROR - ¡No se pudo eliminar al alumno correctamente!')
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))




#############---------FUNCION MODIFICAR------#################

@login_required()
def updateAlumno(request, id_alumno=None): #Actualizar datos alumnos
    template = "actualizar_alumno.html"

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id = id_alumno)
            return render(request, template, {'alumno': alumno})

        except Exception as e:
            messages.error(request,"No fue posible modificar alumno. "+repr(e))
            return HttpResponseRedirect(reverse("alumnos:verAlumno", args=[id_alumno]))

    if request.method == 'POST':
        try:
            alumno = Alumno.objects.get(id = id_alumno)

            alumno.nombre = request.POST.get('inputNombre').upper()
            alumno.apellido_paterno = request.POST.get('inputApellidoPaterno').upper()
            alumno.apellido_materno = request.POST.get('inputApellidoMaterno').upper()
            #alumno.sexo = request.POST.get('inputSexo')
            alumno.correo = request.POST.get('inputCorreo')
            alumno.carrera = request.POST.get('inputCarrera')
            alumno.domicilio = request.POST.get('inputDomicilio')
            #alumno.ocupacion = request.POST.get('inputOcupacion')
            alumno.representante_legal = request.POST.get('inputRepresentante')
            alumno.prevision = request.POST.get('inputPrevision')

            alumno.save()
            messages.success(request, '¡Alumno modificado exitosamente!')
            return HttpResponseRedirect(reverse("alumnos:updateAlumno", args=[id_alumno]))
            #return verAlumno('get', id_alumno)

        except Exception as e:
            messages.error(request,"No fue posible modificar alumno. "+repr(e))
            return verAlumno('get', id_alumno)





#############---------FUNCION MOSTRAR------#################

@login_required()
def verAlumno(request, id_alumno=None):

    template = "ver_alumno.html"

    if request.method == 'GET':
        try:
            alumno = Alumno.objects.get(id = id_alumno)
            if Ficha.objects.filter(alumno_id = id_alumno):
                ficha = Ficha.objects.get(alumno_id = id_alumno)
                registros = Registro.objects.filter(ficha_id = ficha.id)
                return render(request, template, {'alumno': alumno, 'ficha': ficha, 'registros': registros})
            return render(request, template, {'alumno': alumno})

        except Exception as e:
            messages.error(request,"No fue posible mostrar alumno. "+repr(e))
            return render(request, "home.html")




#############---------FUNCION LISTAR------#################

@login_required()
def listarAlumnos(request):

    template = "listar_alumnos.html"
    if request.method == 'GET':
        try:
            alumnos = Alumno.objects.all()
            return render(request, template, {'alumnos': alumnos})

        except Exception as e:
            messages.error(request,"No fue posible listar alumnos. "+repr(e))
            return render(request, "home.html")


#############---------FUNCION BUSCAR------#################

@login_required()
def buscarAlumno(request):

    template = "buscar_alumno.html"
    if request.method == 'GET':
        return render(request, template)

    if request.method == "POST":
        try:
            filtro = request.POST.get('inputSearch')
            querys = (Q(nombre__icontains=filtro) | Q(apellido_materno__icontains=filtro))
            querys |= Q(apellido_paterno__icontains=filtro)
            querys |= Q(rut__icontains=filtro)

            alumnos = Alumno.objects.filter(querys)

            if not alumnos:
                messages.info(request,"No se encontró ningún alumno.")
                return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))
            else:
                return render(request, template, {'alumnos': alumnos})

        except Exception as e:
            messages.error(request,"No se pudo realizar la búsqueda. "+repr(e))
            return HttpResponseRedirect(reverse("alumnos:buscarAlumno"))


#############---------FUNCION CARGAR DATOS CSV------#################

@login_required()
def importAlumnos(request): #Importar alumnos nuevos desde archivo .csv

    template = "alumnos_upload.html"

    if request.method == 'GET':
        return render(request, template)

    if request.method == 'POST':
        try:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith('csv'):
                messages.error(request,'ERROR - ¡No es un archivo .csv!')
                return HttpResponseRedirect(reverse("alumnos:importAlumnos"))
            #if csv_file.multiple_chunks():
            #    messages.error(request,"Archivo es demasiado grande (%.2f MB)." % (csv_file.size/(1000*1000),))
            #    return HttpResponseRedirect(reverse("alumnos:importAlumnos"))
            file_data = csv.reader(codecs.iterdecode(csv_file, 'utf-8'),  delimiter='\t', quoting=csv.QUOTE_NONE)
            row_count = 0
            headers_final = []
            header_split = []
            for row in file_data:
                #print(row)
                row_count += 1
                if 7 > row_count > 3 :
                    header_split = header_split + row[0].split(';')
                if row_count == 6:
                    for h in header_split:
                        string = h.replace('"', '')
                        if string == '(Fijo / Movil)' or string == '':
                            continue
                        headers_final.append(string)

                    #print(headers_final)
                    #print(len(headers_final))

                if row_count > 7:

                    if row[0] == ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;":
                        break

                    dato = row[0].split(";")
                    #print (dato)
                    #print (len(dato)) #deben ser 30
                    cedula = ""
                    primer_nombre = ""
                    segundo_nombre = ""
                    ap_paterno = ""
                    ap_materno = ""
                    correo = ""
                    sexo = ""
                    carrera = ""
                    for header in headers_final:
                        if header == "Carrera":
                            carrera = dato[headers_final.index(header)]
                            #print(carrera)
                        if header == "Rut":
                            rut = dato[headers_final.index(header)]
                            cedula = rut
                            #print(rut)
                        if header == "Dv":
                            dv = dato[headers_final.index(header)]
                            cedula = cedula + "-" + dv
                            #print(dv)
                        if header == "1er Nombre":
                            primer_nombre = dato[headers_final.index(header)]
                            #print(primer_nombre)
                        if header == "2do Nombre":
                            segundo_nombre = dato[headers_final.index(header)]
                            #print(segundo_nombre)
                        if header == "Ap. Paterno":
                            ap_paterno = dato[headers_final.index(header)]
                            #print(ap_paterno)
                        if header == "Ap. Materno":
                            ap_materno = dato[headers_final.index(header)]
                            #print(ap_materno)
                        if header == "Email Personal":
                            correo = dato[headers_final.index(header)]
                            #print(correo)
                        if header == "Sexo":
                            sexo = dato[headers_final.index(header)]
                            #print(sexo)

                    alumnoExiste = Alumno.objects.filter(rut=cedula)
                    if not alumnoExiste:
                        alumno = Alumno()
                        alumno.nombre = primer_nombre
                        if segundo_nombre != "":
                            alumno.nombre = alumno.nombre + " " + segundo_nombre
                        alumno.apellido_paterno = ap_paterno
                        alumno.apellido_materno = ap_materno
                        alumno.rut = cedula
                        alumno.tipoDocumento = "CEDULA"
                        if sexo == "F":
                            alumno.sexo = "Mujer"
                        else:
                            alumno.sexo = "Hombre"
                        alumno.correo = correo
                        alumno.carrera = carrera
                        print(alumno)
                        alumno.save()
                        del alumno
                        print("Guardó al alumno número" + " " + str((row_count-7)))
                    else:
                        alumnoExiste[0].carrera = carrera
                        alumnoExiste[0].save()
                        print("Guardó al alumno número" + " " + str((row_count-7)))
                        del alumnoExiste


                #if row_count == 1:
                #    break

            messages.success(request, '¡Importación exitosa!')

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"ERROR - No se pudo subir archivo. "+repr(e))
            return HttpResponseRedirect(reverse("alumnos:importAlumnos"))


        return HttpResponseRedirect(reverse("alumnos:importAlumnos"))
