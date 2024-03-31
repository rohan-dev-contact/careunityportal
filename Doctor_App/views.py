
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from patient_app.models import Patient,User
from .forms import PatientRegistrationForm
import random
import string
from django.core.mail import send_mail

# Create your views here.
@login_required
def doctorDash(request):
    return render(request, 'Doctor_App/home.html')

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
    return render(request, 'Doctor_App/patient_list.html', {'patients': patients, 'search_query': search_query, 'search_criteria': search_criteria})


@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'Doctor_App/patient_details.html', {'patient': patient})


def add_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            username = 'PT_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))  # Generate random username prefixed with "PT_"
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Generate random password
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
                date_of_birth=form.cleaned_data['date_of_birth'],
                health_condition=form.cleaned_data['health_condition'],
                health_insurance=form.cleaned_data['health_insurance'],
                gender=form.cleaned_data['gender']
            )
            patient.save()
            print(username)
            print(password)
            # Send email to patient
            send_mail(
                'Welcome to CareUnity Portal',
                f'Your account has been created. Your username is: {username}. Your password is: {password}. Please login to access your account.',
                'rohan19mondal@gmail.com',
                [user.email],
                fail_silently=True,
            )
            return redirect('patient_list')
    else:
        form = PatientRegistrationForm()
    return render(request, 'Doctor_App/add_patient.html', {'form': form})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, user_id=patient_id)
    patient.delete()
    # You may also want to add a success message here using Django's messages framework
    return redirect('patient_list')

def edit_patient(request, patient_id):
    # Dummy edit logic
    return redirect('patient_detail', patient_id=patient_id)