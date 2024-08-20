import datetime
from email.policy import default
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db import models
from django_enum_choices.fields import EnumChoiceField
import uuid
import secrets

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

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
    
class Semester_Status(Enum):
    Semester_1 = '1-1'
    Semester_2 = '1-2'
    Semester_3 = '2-1'
    Semester_4 = '2-2'
    Semester_5 = '3-1'
    Semester_6 = '3-2'
    Semester_7 = '4-1'
    Semester_8 = '4-2'

class Application_Status(Enum):
    Pending = 'pending'
    Approved = 'approved'
    Rejected = 'rejected'



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    fullName = models.CharField(max_length=400, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True, null=True)
    entryDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullName


# class Address(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
#     addressName = models.CharField(max_length=400, blank=True)
#     streetAddress = models.CharField(max_length=100)
#     area = models.CharField(max_length=100, blank=True)
#     city = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.streetAddress}, {self.area}, {self.city}, {self.country}"

#     class Meta:
#         verbose_name_plural = 'Addresses'



class Hall(models.Model):
    name = models.CharField(max_length=50)
    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=10, decimal_places=0)
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


class DormitoryApplications(models.Model):
    # Add fields for application details
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(default=secrets.token_urlsafe, max_length=64, unique=True)
    session = models.ForeignKey(Session, on_delete=models.RESTRICT)
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    semester = EnumChoiceField(Semester_Status, default=Semester_Status.Semester_1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    preferred_room = models.ForeignKey(Room, on_delete=models.RESTRICT, blank=True, null=True)

    registration_number = models.CharField(max_length=20)
    fullName = models.CharField(max_length=400)
    birthDate = models.DateField()
    gender = models.CharField(choices=GENDER, max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField()
    picture = models.ImageField(upload_to='ApplicationImages')
    idCardPicture = models.ImageField(upload_to='ApplicationImages', blank=True, null=True)
    # medical_certificate = models.ImageField(upload_to='ApplicationImages')

    guardian_name = models.CharField(max_length=400)
    guardian_relation = models.CharField(max_length=400)
    guardian_phone = PhoneNumberField()
    guardian_address = models.CharField(max_length=400)

    application_status = EnumChoiceField(Application_Status, default=Application_Status.Pending)
    application_date = models.DateTimeField()
    remarks = models.TextField()
    review_date = models.DateTimeField(blank=True, null=True)


class Student(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank = True, null=True)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    
    session = models.ForeignKey(Session, on_delete=models.RESTRICT)
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    semester = EnumChoiceField(Semester_Status, default=Semester_Status.Semester_1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)

    registration_number = models.CharField(max_length=20)
    fullName = models.CharField(max_length=400)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField()
    picture = models.ImageField(upload_to='ApplicationImages')
    idCardPicture = models.ImageField(upload_to='ApplicationImages', blank=True, null=True)

    guardian_name = models.CharField(max_length=400)
    guardian_relation = models.CharField(max_length=400)
    guardian_phone = PhoneNumberField()
    guardian_address = models.CharField(max_length=400)

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


