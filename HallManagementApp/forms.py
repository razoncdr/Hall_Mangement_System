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