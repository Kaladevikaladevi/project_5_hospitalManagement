from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from home.models import Department, Doctors
from .forms import BookingForm


# Home page
def home(request):
    return render(request, 'home.html')


# About page
def about(request):
    return render(request, 'about.html')


# Contact page
def contact(request):
    return render(request, 'contact.html')


# Departments page
def departments(request):
    dept = Department.objects.all()
    return render(request, 'departments.html', {'dept': dept})


# Doctors page
def doctors(request):
    docs = Doctors.objects.all()
    return render(request, 'doctors.html', {'docs': docs})


# Booking page (FINAL)
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # 📧 Email to Admin
            subject = f'New Appointment - {booking.patient_name}'
            message = f"""
New booking details:

Name: {booking.patient_name}
Email: {booking.patient_email}
Phone: {booking.patient_phone}
Doctor: {booking.doctor}
Date: {booking.appointment_date}
Time: {booking.appointment_time}
"""

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['kaladevins9@gmail.com'],  # 🔁 replace with your email
                fail_silently=False,
            )

            # 📧 Confirmation to Patient
            send_mail(
                "Appointment Confirmation",
                f"Hello {booking.patient_name}, your appointment with {booking.doctor} on {booking.appointment_date} is confirmed.",
                settings.EMAIL_HOST_USER,
                [booking.patient_email],
                fail_silently=False,
            )

            # ✅ Success message
            messages.success(request, "Appointment booked successfully!")

            return redirect('booking')

    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})