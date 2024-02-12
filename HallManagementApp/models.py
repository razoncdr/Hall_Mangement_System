# from django.db import models

# Create your models here.
# class Batch(models.Model):
#     batch_title = models.CharField(max_length=50)
    


# class Session(models.Model):
#     session = models.CharField(max_length=50)


# class Department(models.Model):
#     dept_name = models.CharField(max_length=50)


# class Student(models.Model):
#     name = models.CharField(max_length=50)
#     batch = models.IntegerField()
#     department = models.CharField(max_length=50)
#     room_no = models.IntegerField()
#     description = models.TextField()


# class UserProfile(models.Model):
#     name = models.CharField(max_length=50)
#     batch = models.IntegerField()
#     department = models.CharField(max_length=50)
#     room_no = models.IntegerField()
#     about_student = models.TextField()


# Entities:
# 
#     - Batch(title)
#     - Session() 
#     - Department() 
#     - Student() 
#     - UserProfile() 

#     - ApplicationForm(batch, session, dept, regi no, status{approved, pending, rejected, paid}, payment) 
#     - Payment(transactionID, date, amount) 


from django.contrib.auth.models import User
from django.db import models

from core.models import UserProfile


STATUS = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

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

class Student(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank = True, null=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
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


# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     registration_number = models.CharField(max_length=20, unique=True)
#     batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
#     department = models.ForeignKey(Department, on_delete=models.RESTRICT)
#     session = models.ForeignKey(Session, on_delete=models.RESTRICT)
#     status = models.CharField(choices=STATUS, max_length=20, default='active')  # Set default status to 'active'

#     def __str__(self):
#         return f"{self.name} ({self.registration_number})"

class FeesHead(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.amount})"


class StudentFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    feeshead = models.ForeignKey(FeesHead, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class ApplicationForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    # Add fields for application details

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add fields for payment details

