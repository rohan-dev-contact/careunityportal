
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from patient_app.models import Patient,User

# Create your views here.
@login_required
def doctorDash(request):
    return render(request, 'Doctor_App/home.html')

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'Doctor_App/patient_list.html', {'patients': patients})


# @login_required
# def get_patient_details(request, patient_id):
#     print(request)
#     print(patient_id)
#     patient = get_object_or_404(Patient, id=patient_id)
#     user = patient.user
#     # Return user details as JSON response
#     return JsonResponse({
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'email': user.email,
#         # Add other user details here
#     })