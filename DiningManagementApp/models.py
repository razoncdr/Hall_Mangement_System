# models.py
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    # You can add more fields like address, joining_date, etc. as needed

    def __str__(self):
        return self.name

class DiningManager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    shift = models.CharField(max_length=100)
    # You can add more fields like address, experience, etc. as needed

    def __str__(self):
        return self.name
