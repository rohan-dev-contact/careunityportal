from datetime import timedelta,datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from CareUnity_Portal import settings
from Doctor_App.forms import Appointment
from patient_app.forms import OTPVerificationForm, PasswordResetRequestForm, UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from patient_app.models import OTP, Doctor,Patient,User
from django.core.mail import send_mail

# Create your views here.
def home_view(request):
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
    return render(request, 'patient_app/contact.html')

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
    print(request)
    if request.POST:
        form=LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                is_doctor = Doctor.objects.filter(user=user).exists()
                is_patient = Patient.objects.filter(user=user).exists()
                if is_doctor:
                    return redirect('doctor_dashboard')  # Redirect to doctor dashboard
                elif is_patient:
                    return redirect('patient_dashboard')  # Redirect to patient dashboard
                else:
                    return redirect('home')  # Redirect to a general home page
        else: 
            username=form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('password', 'Invalid password.')
            else:
                form.add_error('username', 'Username does not exist.')
    else:
        form=LoginForm()
    return render(request, 'patient_app/registration/login.html', {'forms':form})

def userLogout(request):
    logout(request)
    return redirect('/login')

def appointment(request):
    appointments= Appointment.objects.all()
    return render (request, 'Doctor_App/patient/book_appointment.html',{'appointments':appointments})


# utils.py
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    subject = 'Your OTP for password reset'
    message = f'Your OTP is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

# def passwordResetRequestView(request):
#     if request.method == 'POST':
#         form = PasswordResetRequestForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 # Handle user not found error
#                 return render(request, 'patient_app/registration/reset_password.html', {'form': form, 'error': 'User not found'})

#             otp = generate_otp()
#             # OTP.objects.create(user=user, otp=otp)
#             print(otp)

#             send_otp(user.mobile, otp)  # Assuming send_otp sends the OTP via SMS

#             return redirect(request, 'verify_otp', {'user': user})
#     else:
#         form = PasswordResetRequestForm()
#     return render(request, 'patient_app/registration/reset_password.html', {'form': form})


# def verify_otp(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         user_id = request.session.get('reset_user_id')
#         print(otp,user)
#         if not user_id:
#             return HttpResponseRedirect(reverse('password_reset_request'))
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return HttpResponseRedirect(reverse('password_reset_request'))

#         # Check if the OTP is valid
#         otp_obj = OTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()
#         if otp_obj:
#             # OTP is valid, proceed to reset password
#             # Clear the session
#             del request.session['reset_user_id']
#             return render(request, 'reset_password.html', {'user': user})
#         else:
#             messages.error(request, 'Invalid OTP. Please try again.')
#     return render(request, 'otp_verification.html')


# def verify_otp(request, username):
#     if request.method == 'POST':
#         form = OTPVerificationForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data['otp']
#             user_id = username
#             print(otp, user_id)
#             # Add OTP validation logic here
#             if valid_otp(otp):
#                 # OTP is valid, proceed with password reset
#                 return redirect('reset_password')  # Assuming 'reset_password' is the URL name for the reset password view
#             else:
#                 messages.error(request, 'Invalid OTP. Please try again.')
#     else:
#         form = OTPVerificationForm()
#     return render(request, 'patient_app/registration/otp_verification.html', {'form': form})


# def valid_otp(otp):
#     pass



def passwordResetRequestView(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Handle user not found error
                return render(request, 'patient_app/registration/reset_password.html', {'form': form, 'error': 'User not found'})

            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            send_otp(user.email, otp)  # Assuming send_otp sends the OTP via SMS

            # Redirect to OTP verification view
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
                # Handle user not found error
                return render(request, 'patient_app/registration/reset_password.html', {'form': form, 'error': 'User not found'})

            # Get the latest OTP for the user
            otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()
            if otp_obj and otp_obj.otp == otp:
                # Check if OTP is not expired (within 3 minutes)
                if otp_obj.created_at + timedelta(minutes=3) >= timezone.now():
                    # OTP is valid, proceed with password reset or whatever logic you need
                    print("valid otp")
                    return render(request, 'patient_app/registration/reset_password.html', {'user': user})
                else:
                    messages.error(request, 'OTP has expired. Please request a new OTP.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'patient_app/registration/otp_verification.html', {'form': form})