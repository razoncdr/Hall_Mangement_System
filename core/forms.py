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
    room = ModelChoiceField(queryset=Room.objects.order_by('name').all())
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all())
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all())

    class Meta:
        model = Student
        fields = ["name", "registration_number", "room", "session", "batch", "semester", "department", "status",]
        # widgets = {
        #     "batch": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "session": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "room": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "semester": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "department": forms.Select(attrs={"class": 'form-select-sm',}),
        # }


class StudentFilterForm(forms.Form):
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    room = forms.CharField(label='Room Number', required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',}))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',},))


class StudentFeeForm(forms.Form):
    feesHead = ModelChoiceField(queryset=FeesHead.objects.order_by('-title').all(), widget=forms.Select(attrs={'class':'form-select-sm',},))
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',},))


class StudentFeeFilterForm(forms.Form):
    feesHead = ModelChoiceField(queryset=FeesHead.objects.order_by('-title').all(), required=False,widget=forms.Select(attrs={'class':'form-select-sm',},) )
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-select-sm',},))
    From_Date = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    To_Date = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    payment_Status = forms.ChoiceField(choices=[(None, '------')] + [(tag.value, tag.name) for tag in Payment_Status], 
                                required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))



class StudentFeeStatementForm(forms.Form):
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-select-sm',},))

    

class HallListFilterForm(forms.Form):
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False)

    
# class RoomListFilterForm(forms.Form):
#     room = ModelChoiceField(queryset=Room.objects.all(), required=False)
#     hall = ModelChoiceField(queryset=Hall.objects.all(), required=False)

class RoomListFilterForm(forms.Form):
    room = forms.CharField(label='Room Number', required=False)
    hall = forms.ModelChoiceField(queryset=Hall.objects.all(), label='Hall', required=False)