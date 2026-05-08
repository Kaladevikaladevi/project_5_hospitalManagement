from django.urls import path
from . import views

urlpatterns = [

    # LOGIN PAGE
    path('', views.user_login, name='login'),

    # HOSPITAL WEBSITE
    path('home/', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('booking/', views.booking, name='booking'),

    # AUTHENTICATION
    path('doctor-register/', views.doctor_register, name='doctor_register'),

    path('patient-register/', views.patient_register, name='patient_register'),

    path('logout/', views.user_logout, name='logout'),

    # DASHBOARD
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]