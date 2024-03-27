from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label=("Enter User Name"),
        widget=forms.TextInput(attrs={"class":"form-control form-control-lg", "placeholder":"Enter User Name"})
    )
    first_name = forms.CharField(
        label=("Enter first name"),
        widget=forms.TextInput(attrs={"class": "form-control border-primary", "placeholder":"Enter first name"}),
    )
    last_name = forms.CharField(
        label=("Enter last name"),
        widget=forms.TextInput(attrs={"class": "form-control border-primary", "placeholder":"Enter last name"}),
    )
    email = forms.CharField(
        label=("Enter email-id"),
        widget=forms.EmailInput(attrs={"class": "form-control border-primary", "placeholder":"Enter email-id"}),
    )
    mobile = forms.CharField(
        label=("Enter contact number"),
        widget=forms.NumberInput(attrs={"class": "form-control border-primary", "placeholder":"Enter Contact number"}),
    )
    address = forms.CharField(
        label=("Enter Address"),
        widget=forms.Textarea(attrs={"class": "form-control border-primary", "placeholder":"Enter Address"}),
    )
    password1=forms.CharField(
        label=("Enter Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control border-primary"}),
    )
    password2=forms.CharField(
        label=("Enter Confirm Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control border-primary"}),
    )
    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email","mobile","address")

class MyLogFrm(AuthenticationForm):
    username = forms.CharField(
        label=("Enter user name"),
        widget=forms.TextInput(attrs={"class": "form-control border-primary"}),
    )
    password=forms.CharField(
        label=("Enter Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control border-primary"}),
    )