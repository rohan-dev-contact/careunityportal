
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def doctorDash(request):
    return render(request, 'Doctor_App/home.html')

@login_required
def patientList(request):
    return False