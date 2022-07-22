from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Appointment
from .serializers import AppoitmentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta, datetime



# Create your views here.

@api_view(["GET", "POST"])
def appointment_list(request):

    """
    create new appointment
    Get all appoitments

    """

    if request.method == "GET":
        appoitments = Appointment.objects.all()
        serializer  = AppoitmentSerializer(appoitments, many= True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = AppoitmentSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT","DELETE"])
def appointments_details(request, pk):

    """GET/UPDATE/DLELETE using Id"""
    try:
        appointment = Appointment.objects.get(id=pk)

    except Appointment.DoesNotExist:

        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if (request.method == "GET"):
        serializer = AppoitmentSerializer(appointment)  
        return Response(serializer.data)

    elif (request.method == "PUT"):
        serializer = AppoitmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        appointment.delete()
        return Response(status = status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def appointment_booked_appoitment(request):

    """
    Retrives appointments scheduled for today or in future by filterning on date range and phone number.
    """

    print(request)
    phone = request.query_params.get("phone")
    date_received = request.query_params.get("date")
    print("###########################")
    print(phone)
    print(date_received)

    startdate =  datetime.strptime(date_received, "%Y-%m-%d")
    print(startdate)
    enddate = startdate + timedelta(days=365)

    if request.method == "GET":
        appoitments = Appointment.objects.filter(phone = phone, date__range = [startdate,enddate])
        if (len(appoitments)>0):
            serializer  = AppoitmentSerializer(appoitments, many= True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def check_appoitment(request):

    """
    check if appointment exist for the give slot and date
    """

    slot = request.query_params.get("slot")
    date = request.query_params.get("date")

    print(slot)
    print(date)

    if request.method == "GET":
        appoitments = Appointment.objects.filter(slot = slot, date = date)
        if (len(appoitments)>0):
            serializer  = AppoitmentSerializer(appoitments, many= True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)



def check_slot_available(slot, date):
    appoitments = Appointment.objects.filter(slot = slot, date = date)
    return len(appoitments)



@api_view(["GET"])
def check_next_available_slot(request):

    """
    This function can get  next available slot for the user.
    """

    slot = request.query_params.get("slot")
    date = request.query_params.get("date")

    startdate =  datetime.strptime(date, "%Y-%m-%d")

    print(type(startdate.weekday()))

    for slot_num in range(1, 21):
        if (slot_num <= int(slot))  or startdate.weekday() ==6:
            continue
        else:
            if(check_slot_available(slot_num, date)==0):
                return Response({'slot':slot_num, 'date':date})

        
    print(startdate)
    enddate = startdate + timedelta(days=60)
    startdate = startdate + timedelta(days=1)


    while(startdate != enddate):
        

        if(startdate.weekday()==6):
            startdate = startdate + timedelta(days=1)
            continue
        else:
            for slot_num in range(1, 21):
                if(check_slot_available(slot_num, startdate)==0):
                    print(startdate)
                    print(slot_num)
                    startdate =  datetime.strptime(str(startdate).split()[0],"%Y-%m-%d")
                    return Response({'slot':slot_num, 'date':str(startdate).split()[0]})

        startdate = startdate + timedelta(days=1)
    return Response(status = status.HTTP_404_NOT_FOUND)