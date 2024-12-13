import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Clinic, Patient
from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django_select2.forms import Select2MultipleWidget

ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('clinic', 'Clinic'),
]
SPECIALITY_CHOICES = [
    ('general_practitioner', 'General Practitioner'),
    ('cardiologist', 'Cardiologist'),
    ('dermatologist', 'Dermatologist'),
    ('neurologist', 'Neurologist'),
    ('orthopedic_surgeon', 'Orthopedic Surgeon'),
    ('pediatrician', 'Pediatrician'),
    ('psychiatrist', 'Psychiatrist'),
    ('radiologist', 'Radiologist'),
    ('gynecologist', 'Gynecologist'),
    ('anesthesiologist', 'Anesthesiologist'),
    ('endocrinologist', 'Endocrinologist'),
    ('gastroenterologist', 'Gastroenterologist'),
    ('hematologist', 'Hematologist'),
    ('nephrologist', 'Nephrologist'),
    ('oncologist', 'Oncologist'),
    ('ophthalmologist', 'Ophthalmologist'),
    ('otolaryngologist', 'Otolaryngologist'),
    ('pulmonologist', 'Pulmonologist'),
    ('rheumatologist', 'Rheumatologist'),
    ('urologist', 'Urologist'),
    ('vascular_surgeon', 'Vascular Surgeon'),
    ('plastic_surgeon', 'Plastic Surgeon'),
    ('immunologist', 'Immunologist'),
    ('sports_medicine', 'Sports Medicine Specialist'),
    ('pathologist', 'Pathologist'),
    ('infectious_disease', 'Infectious Disease Specialist'),
    ('nuclear_medicine', 'Nuclear Medicine Specialist'),
    ('emergency_medicine', 'Emergency Medicine Specialist'),
]


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'type': 'password'
        }),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'type': 'password'
        }),
        label='Confirm Password'
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES,
                             widget=forms.Select(attrs={
                                 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
                             }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'role', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'User with the same email already exists')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password or not password2:
            raise forms.ValidationError("Both password fields are required.")

        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

        validate_password(password)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = self.cleaned_data.get('role')

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',

    }))


class ClinicCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        if hasattr(value, 'value'):
            value = value.value
        
        try:
            clinic = Clinic.objects.get(pk=value)
            label = f"{clinic.name} - {clinic.address}"
        except Clinic.DoesNotExist:
            label = str(value)
        
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        
        option['attrs']['class'] = 'mr-2'
        return option
    

class DocRegistration(forms.ModelForm):
    specialty = forms.ChoiceField(
        choices=SPECIALITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        })
    )
    license_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Enter License Number'
        }),
        required=True
    )
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Enter Pincode'
        }),
        required=True
    )

    clinics = forms.ModelMultipleChoiceField(
        queryset=Clinic.objects.all(),
        required=False,
        widget=Select2MultipleWidget(attrs={
            'class': 'flex flex-col space-y-2 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder':'Select Clinics' 
        }),
        to_field_name='id'  
    )

    class Meta:
        model = Doctor
        fields = ['specialty', 'license_number', 'pincode', 'clinics']

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')

        if not re.match(r'^[A-Z0-9]{5,15}$', license_number):
            raise forms.ValidationError(
                "Invalid license number format. It must be 5-15 characters, alphanumeric.")

        if not self.is_license_registered(license_number):
            raise forms.ValidationError(
                "The license number is not registered or valid.")

        return license_number

    def is_license_registered(self, license_number):
        registered_licenses = ['ABC12345', 'XYZ98765', 'LMN56789']
        return license_number in registered_licenses


class MultiSelectWidget(SelectMultiple):
   
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'multi-select-specialities',
            'multiple': 'multiple'
        })
        super().__init__(*args, **kwargs)

class ClinicRegistration(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Enter Clinic Name'
        }),
        required=True
    )
    registration_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Enter License Number'
        }),
        required=True
    )
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Enter Pincode'
        }),
        required=True
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Clinic Contact'
        }),
        required=True
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Full Address'
        }),
        required=True
    )

    specialty_offered = forms.MultipleChoiceField(
        choices=SPECIALITY_CHOICES,
        widget=Select2MultipleWidget(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Select Specialties Available'
        }),
        required=True
    )

    class Meta:
        model = Clinic
        fields = ['name', 'registration_number', 'pincode', 'contact_number', 'address', 'specialty_offered']

    def is_registered(self, registration_number):
        registered_licenses = ['ABC12345', 'XYZ98765', 'LMN56789']
        return registration_number in registered_licenses
    
class PatientRegistration(forms.ModelForm):
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Your Pincode'
        }),
        required=True
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Phone Number'
        }),
        required=True
    )
    
    date_of_birth = forms.DateField(
    widget=forms.DateInput(attrs={
        'type': 'date',  # Enables the browser's calendar widget
        'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        'placeholder': 'Select your Date of Birth'
    }),
    required=True
    )

    medical_history = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Medical History if any (optional)'
        }),
    )

    class Meta:
        model = Patient  # Correct model
        fields = ['pincode', 'phone_number', 'date_of_birth', 'medical_history']  # Relevant fields

    def is_registered(self, registration_number):
        registered_licenses = ['ABC12345', 'XYZ98765', 'LMN56789']
        return registration_number in registered_licenses