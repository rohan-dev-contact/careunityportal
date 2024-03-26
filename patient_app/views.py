from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

