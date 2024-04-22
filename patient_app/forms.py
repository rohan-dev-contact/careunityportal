import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm
from patient_app.models import Appointment, Doctor, User

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label=("Enter User Name"),
        widget=forms.TextInput(attrs={"class":"form-control mt-1 form-control-lg", "placeholder":"Enter User Name"})
    )
    first_name = forms.CharField(
        label=("Enter first name"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter first name"}),
    )
    last_name = forms.CharField(
        label=("Enter last name"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter last name"}),
    )
    email = forms.CharField(
        label=("Enter email-id"),
        widget=forms.EmailInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter email-id"}),
    )
    mobile = forms.CharField(
        label=("Enter contact number"),
        widget=forms.NumberInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter Contact number"}),
    )
    address = forms.CharField(
        label=("Enter Address"),
        widget=forms.Textarea(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter Address"}),
    )
    password1=forms.CharField(
        label=("Enter Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1 border-primary"}),
    )
    password2=forms.CharField(
        label=("Enter Confirm Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1 border-primary"}),
    )
    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email","mobile","address")

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=("Enter user name"),
        widget=forms.TextInput(attrs={"class": "form-control border-primary","placeholder":"Enter User Name"}),
    )
    password=forms.CharField(
        label=("Enter Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control border-primary","placeholder":"Enter Password"}),
    )


class PlainTextPasswordUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Enter Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1 border-primary"}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1 border-primary"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email", "is_staff", "is_active", "address", "mobile")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(label=("Username"), max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Username"}))


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}))


class PasswordResetForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user

        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[fieldname].label,
            })

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs['readonly'] = True  # Make patient details read-only
        self.fields['appdate'].widget.attrs['min'] = str(datetime.date.today())  # Set minimum date to today

    def set_initial_department_doctor(self, department_id, doctor_id):
        self.fields['doctor'].queryset = Doctor.objects.filter(departments=department_id)
        self.initial['doctor'] = doctor_id