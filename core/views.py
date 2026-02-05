from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from .logic import *
from .decorators import *
# Create your views here.

#Client/Patient Views
#####

def index(request):
    
    context = {}
    return render(request, 'files/index.html', context)

def YourAppointment(request):
    context = {}
    return render(request, 'files/client_view_your_appointments.html', context)


#End#############


#Staff Views


@login_required
@role_required('staff')
def staff_dashboard(request):
    context = {}
    return render(request, 'files/staff_dashboard.html', context)


@login_required
@role_required('staff')
def make_appointment(request):
    context = {}
    return render(request, 'files/staff_make_appoint.html', context)


@login_required
@role_required('staff')
def staff_view_appointments(request):
    context = {}
    return render(request, 'files/staff_manage_appointments.html', context)

@login_required
@role_required('staff')
def staff_manage_services_and_functions(request):
    context = {}
    return render(request, 'files/staff_functions.html', context)


#End#############


#Dentist Views

@login_required
@role_required('dentist')
def dentist_dashboard(request):
     context = {}
     return render(request, 'files/dentist_dashboard.html', context)

@login_required
@role_required('dentist')
def view_schedule(request):
    context = {}
    return render(request, 'files/dentist_view_their_schedule.html', context)



@login_required
@role_required('dentist')
def grab_patient_data_view_appointment(request):
    context = {}
    return render(request, 'files/dentist_view_their_app_in_detail.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'files/login.html')


#END#############

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')