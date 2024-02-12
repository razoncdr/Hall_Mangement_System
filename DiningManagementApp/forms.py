# forms.py

from django import forms
from .models import DiningManager, Member

class DiningManagerForm(forms.ModelForm):
    class Meta:
        model = DiningManager
        fields = ['name', 'email', 'phone_number']  # Adjust fields as needed

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone_number']  # Adjust fields as needed
