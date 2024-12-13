from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, DocRegistration, ClinicRegistration, PatientRegistration
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Patient, Clinic, CustomUser
from django.contrib.auth.decorators import login_required

#create your views here


def index(request):
    return render(request,'booking/index.html')


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_login')
    else:
        user_form = UserRegistrationForm()
    
    return render(request,'booking/register.html', {'user_form':user_form})

@login_required
def doctorindex(request,id):
    doctor = Doctor.objects.get(id=id)
    return render(request,'booking/doctorindex.html', {'doctor':doctor})

@login_required
def clinicindex(request,id):
    clinic = Clinic.objects.get(id=id)
    return render(request,'booking/clinicindex.html', {'clinic':clinic})

@login_required
def patientindex(request,id):
    patient = Patient.objects.get(id=id)
    return render(request,'booking/patientindex.html', {'patient':patient})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                if user.role == "doctor":
                    doctor, _ = Doctor.objects.get_or_create(user=user)
                    return redirect('docregister', id=doctor.id)
                elif user.role == "clinic":
                    clinic, _ = Clinic.objects.get_or_create(user=user)
                    return redirect('clinicregister', id=clinic.id)
                elif user.role == "patient":
                    patient, _ = Patient.objects.get_or_create(user=user, defaults={'date_of_birth': None})
                    return redirect('patientregister', id=patient.id)
                else:
                    form.add_error(None, 'Invalid user role.')
            else:
                form.add_error(None, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})

def docregister(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    doctor = Doctor.objects.filter(user=request.user).first() or Doctor.objects.filter(id=id, user=request.user).first()
    if doctor is None:
        return redirect("login")

    if doctor.specialty and doctor.license_number and doctor.pincode:
        return redirect('index')

    doc_form = DocRegistration(instance=doctor)

    if request.method == "POST":
        doc_form = DocRegistration(request.POST, instance=doctor)

        if doc_form.is_valid():
            new_doc = doc_form.save(commit=False)
            new_doc.user = request.user  
            new_doc.save()  
            new_doc.clinics.set(doc_form.cleaned_data['clinics'])
            new_doc.save()  

            return redirect('index') 

    return render(request, 'booking/docregister.html', {'doc_form': doc_form, 'doctor': doctor})



def clinicregister(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    clinic = Clinic.objects.filter(user=request.user).first() or Clinic.objects.filter(id=id).first()
    if clinic is None:
        return redirect("login")

    if clinic.specialty_offered and clinic.registration_number and clinic.pincode and clinic.contact_number:
        return redirect('index')

    clinic_form = ClinicRegistration(instance=clinic)
    if request.method == "POST":
        clinic_form = ClinicRegistration(request.POST, instance=clinic)
        if clinic_form.is_valid():
            new_clinic = clinic_form.save(commit=False)
            new_clinic.user = request.user
            new_clinic.save()
            return redirect('index')

    return render(request, 'booking/clinicregister.html', {'clinic_form': clinic_form, 'clinic': clinic})


def patientregister(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    patient = Patient.objects.filter(user=request.user).first() or Patient.objects.filter(id=id).first()
    if patient is None:
        return redirect("login")

    if patient.date_of_birth and patient.pincode and patient.phone_number:
        return redirect('index')

    patient_form = PatientRegistration(instance=patient)
    if request.method == "POST":
        patient_form = PatientRegistration(request.POST, instance=patient)
        if patient_form.is_valid():
            new_patient = patient_form.save(commit=False)
            new_patient.user = request.user
            new_patient.save()
            return redirect('index')

    return render(request, 'booking/patientregister.html', {'patient_form': patient_form, 'patient': patient})
