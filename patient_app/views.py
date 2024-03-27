from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

def contact_view(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

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
    return render(request, 'registration/signup.html', {'forms': form})


def userLogin(request):
    if request.POST:
        form=LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form=LoginForm()
    return render(request, 'registration/login.html', {'forms':form})

def userLogout(request):
    logout(request)
    return redirect('/login')




