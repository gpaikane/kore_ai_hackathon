from django.urls import path
from .views import appointment_list, appointments_details, appointment_booked_appoitment

urlpatterns = [
    path('appointments/', appointment_list),
    path('detail/<int:pk>', appointments_details),
    path('booked/', appointment_booked_appoitment),
    
]
