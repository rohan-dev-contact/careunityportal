from django import forms
from django.contrib.auth.forms import UserCreationForm
from patient_app.models import User,Patient

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=("Enter first name"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter first name"}),
    )
    last_name = forms.CharField(
        label=("Enter last name"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter last name"}),
    )

    age = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "type": "number"})
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

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(
        label=("Select Gender"),
        choices=gender_choices,
        widget=forms.Select(attrs={"class": "form-control mt-1 border-primary"}),
    )
    
    health_condition = forms.CharField(
        label="Enter Health Condition/Initial Diagnosis", 
        required=False,
        widget=forms.Textarea( attrs={"class": "form-control mt-1 border-primary"}))
    
    health_insurance = forms.CharField(
        label=("Enter Health Insurance Details"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter Insurance Details"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    class Meta:
        model = User
        fields = ("first_name","last_name", "email","mobile","address")



class PatientUserUpdateForm(forms.ModelForm):
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
    class Meta:
        model = User
        fields = ("first_name","last_name", "email","mobile","address")


class PatientPatientUpdateForm(forms.ModelForm):

    age = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "type": "number"})
    )

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(
        label=("Select Gender"),
        choices=gender_choices,
        widget=forms.Select(attrs={"class": "form-control mt-1 border-primary"}),
    )
    
    health_condition = forms.CharField(
        label="Enter Health Condition/Initial Diagnosis", 
        required=False,
        widget=forms.Textarea( attrs={"class": "form-control mt-1 border-primary"}))
    
    health_insurance = forms.CharField(
        label=("Enter Health Insurance Details"),
        widget=forms.TextInput(attrs={"class": "form-control mt-1 border-primary", "placeholder":"Enter Insurance Details"}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['assigned_doctor']
    class Meta:
        model = Patient
        fields = ("age", "gender", "health_condition", "assigned_doctor", "health_insurance")
