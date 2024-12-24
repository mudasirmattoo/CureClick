"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from booking import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('register/',views.register, name='register'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('doctor/<int:id>/',views.doctorindex,name='doctorindex'),
    path('clinic/<int:id>/',views.clinicindex,name='clinicindex'),
    path('patient/<int:id>/',views.patientindex,name='  '),
    path('doctorreg/<int:id>/',views.docregister,name='docregister'),
    path('clinicreg/<int:id>/',views.clinicregister,name='clinicregister'),
    path('patientreg/<int:id>/',views.patientregister,name='patientregister'),
    path('createbooking/<int:id>/',views.createbooking,name='createbooking'),
    path('book_appointment/<int:doctor_id>',views.book_appointment,name='book_appointment'),
    path('available_doctors/',views.available_doctors,name='available_doctors'),
    path('clinic/<int:clinic_id>/doctors/', views.clinic_doctors, name='clinic_doctors'),
    path('doctor/<int:doctor_id>/profile/', views.doctor_profile, name='doctor_profile'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('slot-group/<int:group_id>/', views.slot_group, name='slot_group'),
]
