from datetime import date, datetime, timedelta
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Clinic, Patient, TimeSlot, Appointment, TimeSlotGroup
from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django_select2.forms import Select2MultipleWidget
from datetime import date

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
            'placeholder': 'Select Clinics'
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
        fields = ['name', 'registration_number', 'pincode',
                  'contact_number', 'address', 'specialty_offered']

    def is_registered(self, registration_number):
        registered_licenses = ['ABC12345', 'XYZ98765', 'LMN56789']
        return registration_number in registered_licenses


class PatientRegistration(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Phone Number'
        }),
        required=True
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
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
        model = Patient  #
        fields = ['pincode', 'phone_number',
                  'date_of_birth', 'medical_history']

    def is_registered(self, registration_number):
        registered_licenses = ['ABC12345', 'XYZ98765', 'LMN56789']
        return registration_number in registered_licenses

class CreateBooking(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        }),
        required=True
    )
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        }),
        required=True
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        }),
        required=True
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        }),
        required=True
    )
    slot_duration = forms.ChoiceField(
        choices=[
            (15, '15 minutes'),
            (30, '30 minutes'),
            (45, '45 minutes'),
            (60, '1 hour'),
        ],
        initial=30,
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        }),
        required=True
    )
    max_bookings = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        })
    )
    clinics = forms.ModelMultipleChoiceField(
        queryset=Clinic.objects.all(),
        required=False,
        widget=Select2MultipleWidget(attrs={
            'class': 'flex flex-col space-y-2 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
            'placeholder': 'Select Clinics'
        }),
        to_field_name='id'
    )
    
    def save(self, creator):
        doctor = self.cleaned_data['doctor']
        date = self.cleaned_data['date']
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        slot_duration = int(self.cleaned_data['slot_duration'])
        max_bookings = self.cleaned_data['max_bookings']
        clinics = self.cleaned_data['clinics']
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        current_time = start_datetime

        created_slots = []

        slot_group = TimeSlotGroup.objects.create(
            doctor=doctor,
            date=date,
            start_time=start_datetime,
            end_time=end_datetime,
            slot_duration=slot_duration,
            max_bookings=max_bookings,
            clinics=clinics,
            created_by=creator
        )
        
        created_slots = slot_group.get_slots()
        while current_time + timedelta(minutes=slot_duration) <= end_datetime:
            slot_end_time = current_time + timedelta(minutes=slot_duration)

            time_slot = TimeSlot.objects.create(
                doctor=doctor,
                date=date,
                start_time=current_time.time(),
                end_time=slot_end_time.time(),
                is_booked=False,
                max_bookings=max_bookings,
                current_bookings=0,
                clinics=clinics,
                group=slot_group,
                created_by=creator
                
            )
            time_slot.clinics.set(clinics)
            created_slots.append(time_slot)

            # appointment = Appointment.objects.create(
            #     doctor=doctor,
            #     patient=None,  
            #     time_slot=time_slot,
            #     appointment_date=datetime.combine(date, current_time.time()),
            #     start_time=current_time.time(),
            #     end_time=slot_end_time.time(),
            #     slot_duration=slot_duration,
            #     status='available',
            #     is_active=True,
            #     clinic=creator if isinstance(creator, Clinic) else None 
            # )

            current_time = slot_end_time

            # print(f"Created appointment: {appointment.id} for {appointment.appointment_date}")

        return slot_group, created_slots

class AppointmentBookingForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        })
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        })
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(),
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-center',
        })
    )

    def __init__(self, doctor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                doctor=doctor,
                is_booked=False,
                date__gte=date.today()
            )

    def clean(self):
        cleaned_data = super().clean()
        time_slot = cleaned_data.get('time_slot')
        if time_slot and not time_slot.is_available():
            raise forms.ValidationError("This time slot is no longer available")
        return cleaned_data
    
    def save(self, patient):
        appointment = super().save(commit=False)
        appointment.patient = patient
        appointment.is_booked = True
        appointment.save()
        return appointment
    
    def save_time_slot(self, time_slot):
        time_slot.is_booked = True
        time_slot.current_bookings += 1

        time_slot.save()
        return time_slot
    
    def save_appointment(self, appointment):
        appointment.status = 'booked'
        appointment.save()
        return appointment
    
    def save_appointment_and_time_slot(self, appointment, time_slot):
        appointment.time_slot = time_slot
        appointment.save()
        return appointment

    def save_time_slot_and_appointment(self, time_slot, appointment):
        time_slot.is_booked = True
        time_slot.current_bookings += 1
        time_slot.save()
        appointment.time_slot = time_slot
        appointment.save()
        return appointment

