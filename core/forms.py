from django import forms
from django.forms import ModelChoiceField
from .models import *
from HallManagementApp.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
import datetime


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
 
      
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'password']
        widgets = {
            "username": forms.TextInput(attrs={}),
            "password": forms.TextInput(attrs={'type': 'password'}),
        }
        
        
class UserGroupForm(UserCreationForm):
    id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    is_active = models.BooleanField(default=True)
    user = User()
    group = Group()


class FeesHeadForm(forms.ModelForm):
    class Meta:
        model = FeesHead
        fields = ["title", "amount"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "registration_number", "room", "batch" , "department", "session", "status"]


class StudentFeeForm(forms.Form):
    feesHead = ModelChoiceField(queryset=FeesHead.objects.all(), )
    batch = ModelChoiceField(queryset=Batch.objects.all(), required=False)
    registration_number = forms.CharField(max_length=150, required=False)


