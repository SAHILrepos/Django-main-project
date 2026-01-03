from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Appointment

def home(request):
    services = Service.objects.all()
    return render(request, 'bookings/home.html', {'services': services})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def book_appointment(request):
    if request.method == "POST":
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        service = Service.objects.get(id=service_id)
        Appointment.objects.create(
            user=request.user,
            service=service,
            date=date,
            timeslot=time
        )

        subject = 'Appointment Booking Confirmation'
        message = f'Hi {request.user.username}, your appointment for {service.name} on {date} at {time} has been booked successfully and is pending confirmation.'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        
        try:
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(f"Email failed to send: {e}")

        return redirect('user_panel')
    
    services = Service.objects.all()
    return render(request, 'bookings/book_appointment.html', {'services': services})

@login_required
def user_panel(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bookings/user_panel.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.delete()
    return redirect('user_panel')