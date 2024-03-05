from django.db import models

from HallManagementApp.models import Student
from core.models import UserProfile

class Notice(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)  # Automatically set the date when the notice is created
    
    def __str__(self):
        return self.title


class StudentNotice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title