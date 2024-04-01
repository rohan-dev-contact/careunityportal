
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from patient_app.models import Patient,User
from .forms import PatientRegistrationForm ,PatientPatientUpdateForm,PatientUserUpdateForm
import random
import string
from django.core.mail import send_mail

# Create your views here.
@login_required
def doctorDash(request):
    return render(request, 'Doctor_App/doctor/home.html')

@login_required
def patientDash(request):
    return render(request,'Doctor_App/patient/patient_home.html')


@login_required
def patient_list(request):
    search_query = request.GET.get('search', '')
    search_criteria = request.GET.get('search_criteria', 'name')
    
    if search_criteria == 'name':
        users = User.objects.filter(first_name__icontains=search_query)
        patient_ids = [user.id for user in users]
        patients = Patient.objects.filter(user_id__in=patient_ids)
    elif search_criteria == 'username':
        try:
            patient_id = search_query
            patients = Patient.objects.filter(user__username=patient_id)
        except ValueError:
            patients = Patient.objects.none()
    else:
        patients = Patient.objects.none()
    # print(patients)
    return render(request, 'Doctor_App/doctor/patient_list.html', {'patients': patients, 'search_query': search_query, 'search_criteria': search_criteria})


@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, user__username=patient_id)
    return render(request, 'Doctor_App/doctor/patient_details.html', {'patient': patient})


def add_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            username = 'PT' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))  
            password = ''.join(random.choices(string.digits, k=8))

            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                mobile=form.cleaned_data['mobile'],
                address=form.cleaned_data['address']
            )
            patient = Patient(
                user=user,
                health_condition=form.cleaned_data['health_condition'],
                health_insurance=form.cleaned_data['health_insurance'],
                gender=form.cleaned_data['gender'],
                age=form.cleaned_data['age']
            )
            patient.save()
            print(username)
            print(password)
            # Send email to patient
            send_mail(
                'Welcome to CareUnity Portal',
                f'Your account has been created with username: {username} and password: {password}.\n Please login to access your account.',
                'rohan19mondal@gmail.com',
                [user.email],
                fail_silently=True,
            )
            return redirect('patient_list')
    else:
        form = PatientRegistrationForm()
    return render(request, 'Doctor_App/add_patient.html', {'form': form})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, user__username=patient_id)
    patient.delete()
    return redirect('patient_list')

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, user__username=patient_id)
    if request.method == 'POST':
        formPatientUser = PatientUserUpdateForm(request.POST, instance=patient.user)
        formPatient = PatientPatientUpdateForm(request.POST, instance=patient)
        if formPatient.is_valid() and formPatientUser.is_valid():
            formPatient.save()
            formPatientUser.save()
            return redirect('patient_list')  # Redirect to patient list page
    else:
        formPatientUser = PatientUserUpdateForm( instance=patient.user)
        formPatient = PatientPatientUpdateForm( instance=patient)
    return render(request, 'Doctor_App/doctor/edit_patient.html', {'form1': formPatientUser,'form2':formPatient, 'patient_id': patient.user.username})