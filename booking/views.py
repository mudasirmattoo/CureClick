from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, DocRegistration, ClinicRegistration, PatientRegistration, CreateBooking, AppointmentBookingForm
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Patient, Clinic, CustomUser, Appointment, TimeSlotGroup
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.db.models import Q

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
                    doctor = Doctor.objects.get(user=user)
                    if doctor.specialty and doctor.license_number and doctor.pincode:
                        return redirect('profile')
                    return redirect('docregister', id=doctor.id)
                
                elif user.role == "clinic":
                    clinic = Clinic.objects.get(user=user)
                    if clinic.specialty_offered and clinic.registration_number and clinic.pincode and clinic.contact_number:
                        return redirect('profile')
                    return redirect('clinicregister', id=clinic.id)
                
                elif user.role == "patient":
                    patient = Patient.objects.get(user=user)
                    if patient.date_of_birth and patient.pincode and patient.phone_number:
                        return redirect('available_doctors')
                    return redirect('patientregister', id=patient.id)
                
                else:
                    form.add_error(None, 'Invalid user role.')
            else:
                form.add_error(None, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')

@login_required
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


@login_required
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


@login_required
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

@login_required
def createbooking(request, id):
    if not request.user.is_authenticated:
        return redirect("user_login")
    
    creator = Doctor.objects.filter(user=request.user).first() or Clinic.objects.filter(user=request.user).first()
    if creator is None:
        return redirect("user_login")
    
    if request.method == "POST":
        creator_form = CreateBooking(request.POST)
        
        if creator_form.is_valid():
            try:
                created_appointments = creator_form.save(creator=creator)
                
                if created_appointments:
                    messages.success(request, f'Successfully created {len(created_appointments)} appointments')
                    return redirect('profile')
                else:
                    messages.error(request, 'No appointments were created')
            except Exception as e:
                messages.error(request, f'Error creating appointments: {str(e)}')
        else:
            print("Form errors:", creator_form.errors)  
    else:
        initial_data = {'doctor': creator.id} if isinstance(creator, Doctor) else {}
        creator_form = CreateBooking(initial=initial_data)
    
    return render(request, 'booking/createbooking.html', {
        'creator_form': creator_form, 
        'creator': creator
    })
    
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = request.user.patient

    if request.method == 'POST':
        book_form = AppointmentBookingForm(doctor, request.POST)
        if book_form.is_valid():
            time_slot = book_form.cleaned_data['time_slot']
            selected_date = book_form.cleaned_data['date']
            
            if time_slot.book_slot(patient):
                appointment = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    time_slot=time_slot,
                    appointment_date=selected_date,
                    start_time=time_slot.start_time,
                    end_time=time_slot.end_time,
                    status='booked'
                )
                book_form.save_time_slot(time_slot)
                book_form.save_appointment(appointment)
                messages.success(request, 'Appointment booked successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'This slot is no longer available')
    else:
        book_form = AppointmentBookingForm(doctor)

    return render(request, 'booking/book_appointment.html', {
        'book_form': book_form,
        'doctor': doctor
    })


@login_required
def clinic_doctors(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = clinic.doctors.all()
    
    context = {
        'clinic': clinic,
        'doctors': doctors,
    }
    return render(request, 'booking/clinic_doctors.html',context)

@login_required
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'booking/doctor_profile.html', {
        'doctor': doctor
    })


    
@login_required
def profile(request):
    if request.user.role == 'doctor':
        today = date.today()
        slot_groups = TimeSlotGroup.objects.filter(doctor = request.user.doctor).order_by('start_time')
        todays_slots = TimeSlotGroup.objects.filter(doctor = request.user.doctor,date=today).order_by('start_time')
        # created_appointments = Appointment.objects.filter(doctor=request.user.doctor,status='available',patient__isnull=True,appointment_date=today).order_by('appointment_date','start_time')
        booked_appointments = Appointment.objects.filter(doctor=request.user.doctor,status='booked',patient__isnull=False,appointment_date=today).order_by('-appointment_date','-start_time')
        context = {'slot_groups':slot_groups, 'todays_slots':todays_slots, 'booked_appointments':booked_appointments,'user':request.user}
        return render(request, 'booking/profile.html', context)
    
    elif request.user.role == 'clinic':
        today = date.today()
        clinic = Clinic.objects.get(user=request.user)
        doctors = clinic.doctors.all()
        slot_groups = TimeSlotGroup.objects.filter(clinics=clinic).order_by('start_time')
        todays_slots = TimeSlotGroup.objects.filter(clinics=clinic,date=today).order_by('start_time')
        context = {'clinic': clinic, 'doctors': doctors, 'slot_groups':slot_groups, 'todays_slots':todays_slots}
    
    elif request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('appointment_date','start_time')
        context = {'appointments':appointments,'user':request.user}
    
    return render(request, 'booking/profile.html', context)

@login_required
def edit_profile(request):
    return render(request, 'booking/edit_profile.html')



@login_required
def available_doctors(request):
    search_query = request.GET.get('search', '')
    specialty_filter = request.GET.get('specialty', '')
    location_filter = request.GET.get('location', '')

    specialties = set()
    for doctor in Doctor.objects.all():
        specialties.add(doctor.specialty)
    for clinic in Clinic.objects.all():
        specialties.update(clinic.specialty_offered)
    specialties = sorted(list(specialties))

    doctors = Doctor.objects.all()
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(specialty__icontains=search_query)
        )
    if specialty_filter:
        doctors = doctors.filter(specialty__icontains=specialty_filter)
    if location_filter:
        doctors = doctors.filter(pincode=location_filter)

    clinics = Clinic.objects.all()
    if search_query:
        clinics = clinics.filter(
            Q(name__icontains=search_query) |
            Q(specialty_offered__icontains=search_query)
        )
    if specialty_filter:
        clinics = clinics.filter(specialty_offered__icontains=specialty_filter)
    if location_filter:
        clinics = clinics.filter(pincode=location_filter)

    context = {
        'doctors': doctors,
        'clinics': clinics,
        'specialties': specialties,
    }
    
    return render(request, 'booking/available_doctors.html', context)
