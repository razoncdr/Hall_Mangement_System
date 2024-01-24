from email.policy import default
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
# from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

Unit = (
    ('kg', 'KG'),
    ('litre', 'Litre'),
    ('piece', 'Piece'),
    ('feet', 'Feet'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    fullName = models.CharField(max_length=400, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, blank=True, null=True)
    # phone = PhoneNumberField(blank=True)
    entryDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullName


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    addressName = models.CharField(max_length=400, blank=True)
    streetAddress = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.streetAddress}, {self.area}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = 'Addresses'



