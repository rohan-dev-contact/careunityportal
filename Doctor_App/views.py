from datetime import timedelta, timezone
from CareUnity_Portal import settings
from Doctor_App.models import Prescription
from Doctor_App.forms import PrescriptionForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from patient_app.forms import AppointmentForm
from patient_app.models import Appointment, Patient, Schedule,User,Doctor,Department
from Doctor_App.forms import PatientRegistrationForm ,PatientPatientUpdateForm,PatientUserUpdateForm,DepartmentForm
import random
import string
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

"""Views Starts From Here"""
@login_required
def doctorDash(request):
    if request.user.is_authenticated:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        if is_doctor:
            return render(request, 'Doctor_App/doctor/home.html')
        else:
             return redirect('patient_dashboard') 
    else:
        return redirect('login')   


@login_required
def patientDash(request):
    if request.user.is_authenticated:
        is_patient = Patient.objects.filter(user=request.user).exists()
        if is_patient:
            return render(request,'Doctor_App/patient/patient_home.html')
        else:
            return redirect('home')
    else:
        return redirect('login')


@login_required
def patient_list(request):
    try:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        if is_doctor : 
            current_doctor = Doctor.objects.get(user=request.user) if hasattr(request.user, 'doctor') else None
            search_query = request.GET.get('search', '')
            search_criteria = request.GET.get('search_criteria', 'name')

            if search_criteria == 'name' and search_query != '' :
                users = User.objects.filter(first_name__icontains=search_query)
                patient_ids = [user.id for user in users]
                patients = Patient.objects.filter(user_id__in=patient_ids)
            elif search_criteria == 'username' and search_query != '':
                try:
                    patient_id = search_query
                    patients = Patient.objects.filter(user__username=patient_id)
                except ValueError:
                    patients = Patient.objects.none()
            else:
                patients = Patient.objects.all()
                patients = patients.filter(assigned_doctor=current_doctor) | patients.filter(assigned_doctor=None)    

            # Pagination
            paginator = Paginator(patients, 10)  # Show 10 patients per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'Doctor_App/doctor/patient_list.html', {'patients': page_obj, 'search_query': search_query, 'search_criteria': search_criteria})
        else:
            return redirect('patient_dashboard')
    except Exception as e:
        print("Error In Patient List", e)
        return render(request, 'Doctor_App/doctor/home.html')


@login_required
def patient_detail(request, patient_id):
    if request.user.is_authenticated:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        if is_doctor: 
            patient = Patient.objects.get(user__username=patient_id)
            prescriptions = Prescription.objects.filter(patient=patient).order_by('-date')

            paginator = Paginator(prescriptions, 5)
            page_number = request.GET.get('page')
            try:
                prescriptions = paginator.page(page_number)
            except PageNotAnInteger:
                prescriptions = paginator.page(1)
            except EmptyPage:
                prescriptions = paginator.page(paginator.num_pages)
            return render(request, 'Doctor_App/doctor/patient_details.html', {'patient': patient, 'prescriptions': prescriptions})
        else: 
            return redirect('patient_dashboard')
    else:
        return redirect('login')


def add_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # username = 'PT' + ''.join(random.choices(string.ascii_letters.capitalize() + string.digits, k=6))  
            username = 'PT' + ''.join(random.choices(string.digits, k=6))  
            # password = ''.join(random.choices(string.digits, k=8))
            password = '12346789'

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
            # Send email to patient
            send_mail(
                'Welcome to CareUnity Portal',
                f'Your account has been created with username: {username} and password: {password}.\n Please login to access your account.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True,
            )
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'Doctor_App/add_patient.html', {'form': form})


def delete_patient(request, patient_id):
    if request.user.is_authenticated:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        if is_doctor:
            patient = get_object_or_404(Patient, user__username=patient_id)
            patient.delete()
            return redirect('patient_list')
        else:
            return redirect('login')
    else:
        return redirect('login')


def edit_patient(request, patient_id):
    if request.user.is_authenticated:
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
    else:
        return redirect('login')


def add_prescription(request, patient_id, follow_up_id=None):
    if request.user.is_authenticated:
        if  Doctor.objects.filter(user=request.user).exists():
            patient = Patient.objects.get(user__username=patient_id)
            if request.method == 'POST':
                form = PrescriptionForm(request.POST)
                if form.is_valid():
                    prescription = form.save(commit=False)
                    prescription.doctor = request.user
                    prescription.patient = patient
                    prescription.save()
                    if follow_up_id:
                        previous_prescription = Prescription.objects.get(pk=follow_up_id)
                        previous_prescription.follow_up = prescription
                        previous_prescription.save()
                    return redirect('patient_detail', patient_id=patient_id)
            else:
                form = PrescriptionForm()
            return render(request, 'Doctor_App/doctor/add_prescription.html', {'form': form, 'patient': patient})
        else:
            return redirect('patient_dashboard')
    else:
        return redirect('login')


@login_required
def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'Doctor_App/doctor/view_prescription.html', {'prescription': prescription})


@login_required
def edit_prescription(request, prescription_id):
     if request.user.is_authenticated:
        if  Doctor.objects.filter(user=request.user).exists():
            prescription = get_object_or_404(Prescription, id=prescription_id)
            if request.method == 'POST':
                form = PrescriptionForm(request.POST, instance=prescription)
                if form.is_valid():
                    form.save()
                    return redirect('view_prescription', prescription_id=prescription.id)
            else:
                form = PrescriptionForm(instance=prescription)
            return render(request, 'Doctor_App/doctor/edit_prescription.html', {'form': form, 'prescription': prescription})
        else:
            return redirect('home')
     else:
         return redirect('home')


def get_specializations(obj):
    return ', '.join([s.name for s in obj.specialization.all()])

def get_departments(obj):
    return ', '.join([s.department_name for s in obj.departments.all()])

@login_required
def print_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctorDetails = get_object_or_404(Doctor,user_id=prescription.doctor_id)
    dname = get_departments(doctorDetails)
    sname = get_specializations(doctorDetails)
    # print(doctorDetails)
    return render(request, 'Doctor_App/doctor/print_prescription.html', {'prescription': prescription,'doctorDetails':doctorDetails,'dname':dname,'sname':sname})


@login_required
def patient_prescription_list(request):
    patient = request.user.patient  # Assuming the user is logged in and has a patient profile
    prescriptions = patient.prescription_set.all().order_by('-date')

    # Pagination
    paginator = Paginator(prescriptions, 10)  # Show 10 prescriptions per page
    page = request.GET.get('page')
    try:
        prescriptions = paginator.page(page)
    except PageNotAnInteger:
        prescriptions = paginator.page(1)
    except EmptyPage:
        prescriptions = paginator.page(paginator.num_pages)

    return render(request, 'Doctor_App/patient/patient_prescription_list.html', {'prescriptions': prescriptions})


def prescription_details(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'Doctor_App/patient/view_prescription_patient.html', {'prescription': prescription})


def find_doctor(request):
    department_details = None
    doctors = None

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department_id = form.cleaned_data['department']
            department_details = Department.objects.get(pk=department_id)
            doctors_list = Doctor.objects.filter(departments=department_id)
            paginator = Paginator(doctors_list, 10)  # Show 10 doctors per page
            page_number = request.GET.get('page')
            doctors = paginator.get_page(page_number)
    else:
        form = DepartmentForm()
    return render(request, 'Doctor_App/patient/find_doctor.html', {'form': form, 'department_details': department_details, 'doctors': doctors})


def doctor_details(request, doctor_id,department_id):
    doctor = get_object_or_404(Doctor, user_id=doctor_id)
    return render(request, 'Doctor_App/patient/doctor_details.html', {'doctor': doctor,'department_id':department_id})


@login_required
def book_appointment(request, doctor_id, department_id):
    doctor = get_object_or_404(Doctor, user_id=doctor_id)
    patient = request.user.patient  # Assuming user is a patient

    if request.method == 'POST':
        form = AppointmentForm(request.POST, doctor=doctor)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.appdate = form.cleaned_data['appdate']
            appointment.save()
            return redirect('appointment_success', appointment_id=appointment.appid, doctor_id=doctor_id, department_id=department_id)
    else:
        form = AppointmentForm(doctor=doctor)

    return render(request, 'Doctor_App/patient/book_appointment.html', {'form': form, 'doctor': doctor, 'department_id': department_id})

def appointment_success(request, appointment_id, doctor_id, department_id):
    appointment = get_object_or_404(Appointment, appid=appointment_id)
    return render(request, 'Doctor_App/patient/appointment_success.html', {'appointment': appointment, 'doctor_id': doctor_id, 'department_id': department_id})



@login_required
def upcoming_appointments(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('appdate')

    # Pagination
    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')

    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)

    return render(request, 'Doctor_App/patient/upcoming_appointments.html', {'appointments': appointments})