from django import forms
from django.forms import ModelChoiceField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
import datetime



class HallForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Hall
 
        # specify fields to be used
        fields = [
            "name",
        ]


class RoomForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Room
 
        # specify fields to be used
        fields = [
            "hall",
            "name",
        ]



class BatchForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Batch
 
        # specify fields to be used
        fields = [
            "name",
        ]



class DepartmentForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Department
 
        # specify fields to be used
        fields = [
            "name",
        ]


class SessionForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Session
 
        # specify fields to be used
        fields = [
            "name",
        ]


class SemesterForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Semester
 
        # specify fields to be used
        fields = [
            "name",
        ]