from django.db import models

# Create your models here.

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    slot = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name