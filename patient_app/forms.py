import datetime
import random
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm
from patient_app.models import Appointment, Contact, Doctor, Schedule, User

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





class CaptchaField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.captcha_value = self._generate_captcha()
        kwargs['label'] = f'What is {self.captcha_value[0]} + {self.captcha_value[1]}?'
        kwargs['max_length'] = 2
        super().__init__(*args, **kwargs)

    def _generate_captcha(self):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return (a, b)

    def validate(self, value):
        super().validate(value)
        if int(value) != sum(self.captcha_value):
            raise forms.ValidationError('Incorrect answer to CAPTCHA')
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha_answer = forms.IntegerField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # The label for captcha_answer will be set in the view

    def clean_captcha_answer(self):
        request = self.request
        answer = self.cleaned_data.get('captcha_answer')
        correct_answer = request.session.get('captcha_answer')
        if answer != correct_answer:
            raise forms.ValidationError("Incorrect CAPTCHA answer.")
        return answer



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
        fields = ['appdate']
        widgets = {
            'appdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor')
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['appdate'].label = 'Appointment Date'
        self.fields['appdate'].error_messages = {'required': 'Please select a date.'}
        self.fields['appdate'].validators.append(self.validate_appdate)

        # Get available dates for the doctor
        schedules = Schedule.objects.filter(doctor=doctor)
        self.available_dates = [schedule.days for schedule in schedules]

    def validate_appdate(self, value):
        if value.strftime('%A') not in self.available_dates:
            raise forms.ValidationError('The selected date is not available. Please choose a date when the doctor is available.')
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


