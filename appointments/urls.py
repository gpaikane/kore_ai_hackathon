from django.urls import path
from .views import appointment_list, appointments_details, appointment_booked_appoitment,check_appoitment, check_next_available_slot

urlpatterns = [
    path('appointments/', appointment_list),
    path('detail/<int:pk>', appointments_details),
    path('booked/', appointment_booked_appoitment),
    path('checkslot/', check_appoitment),
    path('check_availbale_slot/',check_next_available_slot),
    
]
