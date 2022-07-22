from attr import field
from rest_framework import serializers
from .models import Appointment

"""
class AppoitmentSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=100)
    phone = serializers.IntegerField()
    slot = serializers.IntegerField()
    date = serializers.DateField()


    def create(self, instance,  validated_data):
        return Appointment.objects.create(validated_data)

    def update(self, instance, validated_data ):

        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.slot = validated_data.get('slot', instance.slot)                
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

"""


class AppoitmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ['id','name', 'phone', 'slot', 'date']