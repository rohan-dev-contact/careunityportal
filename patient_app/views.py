from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import random

from CareUnity_Portal import settings
# from Doctor_App.forms import Appointment
from patient_app.forms import AppointmentForm, ContactForm, OTPVerificationForm, PasswordResetForm, PasswordResetRequestForm, UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from patient_app.models import OTP, Appointment, Doctor,Patient, Schedule,User
from django.core.mail import send_mail

# Create your views here.
def home_view(request):
    return render(request, 'patient_app/home.html')

def dashboard(request):
    if request.user.is_authenticated:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        is_patient = Patient.objects.filter(user=request.user).exists()
        if is_doctor:
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard
        if is_patient:
            return redirect('patient_dashboard')  # Redirect to patient dashboard
    return render(request, 'patient_app/home.html')

def about_view(request):
    return render(request, 'patient_app/about.html')

def services_view(request):
    return render(request, 'patient_app/services.html')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'patient_app/contact.html', {'form': form})

def terms(request):
    return render(request, 'patient_app/terms.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration is successfull')
            except:
                messages.error(request, 'Registration is unsuccessfull')
            return redirect('login') 
        else:
            print("Form is not valid")
    else:
        form = UserRegistrationForm()
    return render(request, 'patient_app/registration/signup.html', {'forms': form})

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.request = request  # Pass the request to the form for CAPTCHA validation
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                is_doctor = Doctor.objects.filter(user=user).exists()
                is_patient = Patient.objects.filter(user=user).exists()
                if is_doctor:
                    return redirect('doctor_dashboard')
                elif is_patient:
                    return redirect('patient_dashboard')
                else:
                    return redirect('home')
            else:
                form.add_error('password', 'Invalid password.')
        else:
            # Regenerate CAPTCHA question
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            request.session['captcha_answer'] = num1 + num2
            form.fields['captcha_answer'].label = f"What is {num1} + {num2}?"

            # Display errors
            return render(request, 'patient_app/registration/login.html', {'form': form})
    else:
        form = LoginForm()

        # Generate a new CAPTCHA question
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        request.session['captcha_answer'] = num1 + num2
        form.fields['captcha_answer'].label = f"What is {num1} + {num2}?"

    return render(request, 'patient_app/registration/login.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('/login')

def appointment(request):
    pass
    # if request.method=='POST':
    #     form=Appointment_form(request.POST)
    #     if form.is_valid():
    #         appt=form.save(commit=False)
    #         appt.user=request.user
    #         appt.save()
    #         return redirect('appointment booked successfully !')
    #     else:
    #         form=Appointment_form()
    #         return render(request,'Doctor_App/patient/book_appointment.html',{'form':form})
        
        
    
    return render (request, 'Doctor_App/patient/book_appointment.html',{'appointment':appointment})

# def select_dept(request):
#     if request.method=='POST':
#         form= Dept_Selection_Form(request.POST)
#         if form.is_valid():
#             selected_dept= form.cleaned_data['departments']
#             doctors= Doctor.objects.filter(departments=selected_dept)
#             return render(request,'Doctor_App/doctor/doctor_list.html',{'doctors':doctors})
#         else:
#             form=Dept_Selection_Form()
#             return render(request, 'Doctor_App/doctor/select_dept.html', {'form':form})

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')  # Redirect to a success page
    else:
        form = FileUploadForm()
    return render(request, 'Doctor_App/patient/report_upload.html', {'form': form})




def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    subject = 'Your OTP for password reset'
    message = f'Your OTP is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])




def passwordResetRequestView(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, 'patient_app/registration/reset_password.html', {'form': form, 'error': 'User not found'})

            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            send_otp(user.email, otp)
            return redirect('verify_otp', username=username)
    else:
        form = PasswordResetRequestForm()
    return render(request, 'patient_app/registration/reset_password.html', {'form': form})

def verify_otp(request, username):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, 'patient_app/registration/reset_password.html', {'form': form, 'error': 'User not found'})
            
            otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()
            if otp_obj and otp_obj.otp == otp:
                if otp_obj.created_at + timedelta(minutes=3) >= timezone.now():
                    return redirect('reset_password', username=username)
                else:
                    messages.error(request, 'OTP has expired. Please request a new OTP.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'patient_app/registration/otp_verification.html', {'form': form})



def reset_password(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'patient_app/registration/reset_password.html', {'error': 'User not found'})

    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Authenticate the user and log them in
            user = authenticate(request, username=username, password=form.cleaned_data['new_password1'])
            if user is not None:
                login(request, user)
                # Redirect to a success page or the login page
                return redirect('login')
    else:
        form = PasswordResetForm(user)
    return render(request, 'patient_app/registration/set_password.html', {'form': form})


