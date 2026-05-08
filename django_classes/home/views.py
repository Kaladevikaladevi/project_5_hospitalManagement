from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from home.models import Department, Doctors
from .forms import BookingForm, PatientRegisterForm, DoctorRegisterForm

from .models import MedicalReport
from .forms import MedicalReportForm


# =========================
# AUTHENTICATION VIEWS
# =========================

def user_login(request):

    # If already logged in
    if request.user.is_authenticated:

        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')

        elif request.user.role == 'patient':
            return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == 'doctor':
                return redirect('doctor_dashboard')

            elif user.role == 'patient':
                return redirect('home')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

def user_logout(request):

    logout(request)

    return redirect('login')


# =========================
# REGISTRATION VIEWS
# =========================

def patient_register(request):

    form = PatientRegisterForm()

    if request.method == 'POST':

        form = PatientRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = 'patient'
            user.save()

            return redirect('login')

        else:
            print(form.errors)

    return render(request, 'patient_signup.html', {'form': form})

def doctor_register(request):

    form = DoctorRegisterForm()

    if request.method == 'POST':

        form = DoctorRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = 'doctor'
            user.save()

            return redirect('login')

        else:
            print(form.errors)

    return render(request, 'doctor_signup.html', {'form': form})

# =========================
# HOSPITAL WEBSITE PAGES
# =========================

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='login')
def departments(request):

    dept = Department.objects.all()

    return render(request, 'departments.html', {
        'dept': dept
    })


@login_required(login_url='login')
def doctors(request):

    docs = Doctors.objects.all()

    return render(request, 'doctors.html', {
        'docs': docs
    })


# =========================
# BOOKING SYSTEM
# =========================

@login_required(login_url='login')
def booking(request):

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save()

            # =========================
            # EMAIL TO ADMIN
            # =========================

            subject = f'New Appointment - {booking.patient_name}'

            message = f"""
New booking details:

Patient Name: {booking.patient_name}
Patient Email: {booking.patient_email}
Patient Phone: {booking.patient_phone}

Doctor: {booking.doctor}

Appointment Date: {booking.appointment_date}
Appointment Time: {booking.appointment_time}
"""

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['kaladevins9@gmail.com'],
                fail_silently=False,
            )

            # =========================
            # CONFIRMATION EMAIL
            # =========================

            send_mail(
                'Appointment Confirmation',
                f"""
Hello {booking.patient_name},

Your appointment with {booking.doctor}
on {booking.appointment_date}
at {booking.appointment_time}
has been confirmed.

Thank You.
""",
                settings.EMAIL_HOST_USER,
                [booking.patient_email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Appointment booked successfully!"
            )

            return redirect('booking')

    else:

        form = BookingForm()

    return render(request, 'booking.html', {
        'form': form
    })


# =========================
# DOCTOR DASHBOARD
# =========================

@login_required(login_url='login')
def doctor_dashboard(request):

    # Block patients
    if request.user.role != 'doctor':
        return redirect('home')

    return render(request, 'doctor_dashboard.html')


# =========================
# REPORT UPLOAD
# =========================

@login_required(login_url='login')
def upload_report(request):

    if request.method == "POST":

        uploaded_file = request.FILES.get("report")

        if uploaded_file:

            MedicalReport.objects.create(
                patient=request.user,
                report_name=uploaded_file.name,
                report_file=uploaded_file
            )

            messages.success(request, "Medical report uploaded successfully!")

            return redirect('upload_report')

        else:
            messages.error(request, "Please select a file.")

    return render(request, 'upload_report.html')


# =========================
# VIEW REPORTS
# =========================

@login_required(login_url='login')
def view_reports(request):

    if request.user.role != 'doctor':

        return redirect('home')

    reports = MedicalReport.objects.all()

    return render(
        request,
        'view_reports.html',
        {'reports': reports}
    )


@login_required(login_url='login')
def doctor_dashboard(request):

    if request.user.role != 'doctor':
        return redirect('home')

    return render(
        request,
        'doctor_dashboard.html'
    )