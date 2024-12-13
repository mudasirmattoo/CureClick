from django.contrib import admin
from .models import CustomUser, Patient, Doctor, Appointment, Clinic, TimeSlot, MedicalRecord
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Clinic)
admin.site.register(TimeSlot)
admin.site.register(MedicalRecord)
