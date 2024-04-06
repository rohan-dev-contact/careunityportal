from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from .models import Doctor,Patient,User#,Appointment


# Create your views here.
def home_view(request):
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
    







