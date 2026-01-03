from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), 
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.user_panel, name='user_panel'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]