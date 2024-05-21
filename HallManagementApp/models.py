from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db import models
from django_enum_choices.fields import EnumChoiceField
from core.models import UserProfile


STATUS = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

Transaction_Type = (
    ('cash', 'Cash'),
    ('bkash', 'Bkash'),
    ('rocket', 'Rocket'),
    ('nagad', 'Nagad'),
)

class Payment_Status(Enum):
    PAID = 'P'
    UNPAID = 'U'

class Hall(models.Model):
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name} ({self.hall})"

class Batch(models.Model):
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Session(models.Model):
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Semester(models.Model):
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Student(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank = True, null=True)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20)
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    session = models.ForeignKey(Session, on_delete=models.RESTRICT)
    status = models.CharField(choices=STATUS, max_length=20)
    # Add other attributes related to a student

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class FeesHead(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.amount})"


class StudentFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    feeshead = models.ForeignKey(FeesHead, on_delete=models.RESTRICT)
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    #paymentStatus = models.CharField(choices=Payment_Status, default=Payment_Status.PAID, max_length=20)
    paymentStatus = EnumChoiceField(Payment_Status, default=Payment_Status.UNPAID)
    entryuser = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    entryDate = models.DateTimeField(null=True, blank=True)


class FeeTransaction(models.Model):
    studentFee =  models.ManyToManyField('StudentFees', related_name='transactions')
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    entryDate = models.DateTimeField()
    transactionType = models.CharField(choices=Transaction_Type, max_length=20)
    transactionId = models.CharField(max_length=100)
    transactionDetails = models.TextField()


class ApplicationForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    # Add fields for application details

