from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')   

def contact(request):
    return render(request, 'contact.html')

def departments(request):
    return render(request, 'departments.html')    

def doctors(request):
    return render(request, 'doctors.html')

def booking(request):
    return render(request, 'booking.html')
