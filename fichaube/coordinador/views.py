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
