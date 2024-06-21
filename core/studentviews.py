from sqlite3 import Timestamp
from unicodedata import category, name
from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from .models import *
from HallManagementApp.models import *
from .forms import *
from .decorators import *
import datetime
import random
import string
import json
from django.db.models import Q


def dormitoryApplicationCreate(request):
    message = ""
    if request.method == 'POST':
        form = DormitoryApplicationsForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an instance of the form but don't save it yet
            instance = form.save(commit=False)
            instance.application_status = Application_Status.Pending
            instance.application_date = timezone.now()
            instance.save()

            message = "Form Submitted Successfully!!"
        else:
            # Form is invalid, handle the validation errors
            errors = form.errors.as_data()
            # You can print errors to debug or log them
            print(errors)
            # In a real application, you might want to do something more user-friendly
            # For simplicity, we'll just update the message to indicate validation errors
            message = "Form submission failed due to validation errors."
    else:
        form = DormitoryApplicationsForm()

    context = {}
    context["message"] = message
    context["form"] = form

    return render(request, 'dormitoryApplications/dormitoryform.html', context)