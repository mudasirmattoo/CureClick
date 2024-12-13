import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

PINCODE_VALIDATOR = RegexValidator(
    regex=r'^\d{6}$',
    message="Pincode must be exactly 6 digits."
)


ROLE_CHOICES = [
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
    ('clinic', 'Clinic'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Clinic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=6, validators=[PINCODE_VALIDATOR])
    contact_number = models.CharField(max_length=15)
    specialty_offered = models.JSONField(default=list)
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6, validators=[PINCODE_VALIDATOR])
    start_time = models.TimeField(null=False, blank=False, default="09:00:00")
    end_time = models.TimeField(null=False, blank=False, default="09:30:00")
    clinics = models.ManyToManyField(Clinic, blank=True, related_name='doctors')

    
    def get_available_slots(self,interval_minutes=30):
        slots = []
        current_time = datetime.datetime.combine(datetime.today(),self.start_time)
        end_time = datetime.datetime.combine(datetime.today(),self.end_time)
        
        
        while current_time < end_time:
            next_time = current_time + datetime.timedelta(minute=interval_minutes)
            slots.append(f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}")
            current_time = next_time
    
        return slots
  
class Patient(models.Model):    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[PINCODE_VALIDATOR])
    phone_number = models.CharField(max_length=12, default='', blank=True)
    def __str__(self):
        return self.user.username
    
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    patient = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.appointment_date}"

    def appointment_booking(self):
        if self.time_slot.is_booked:
            raise ValueError("This time slot has benn already booked.")
        
        self.time_slot.is_booked = True
        self.time_slot.patient = self.patient
        self.time_slot.save()
        
        
        self.status = 'booked'
        self.save()
        
    def cancel_appointment(self):
        self.time_slot.is_booked = False
        self.time_slot.patient = None
        self.time_slot.save()
        self.status = 'canceled'
        self.save()
        
        

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    diagnoses = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical record of {self.patient.user.username}"