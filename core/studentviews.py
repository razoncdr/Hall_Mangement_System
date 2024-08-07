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

            messages.success(request, 'Form Submitted Successfully!!.')

        else:
            # Form is invalid, handle the validation errors
            errors = form.errors.as_data()
            # You can print errors to debug or log them
            # print(errors)
            # In a real application, you might want to do something more user-friendly
            # For simplicity, we'll just update the message to indicate validation errors            
            messages.error(request, "Form submission failed due to validation errors.")
    else:
        form = DormitoryApplicationsForm()

    context = {}
    context["message"] = message
    context["form"] = form

    return render(request, 'dormitoryApplications/dormitoryform.html', context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def dormitoryApplication_list(request):
    applications = DormitoryApplications.objects.none()

    form = DormitoryApplicationsFilterForm(request.POST or None)    
    if request.method == "POST":
        if form.is_valid():
            applications = DormitoryApplications.objects.filter(
                            application_date__gte=form.cleaned_data['date_from'], 
                            application_date__lte=form.cleaned_data['date_to']).all()

            if form.cleaned_data.get('session'):
                applications = applications.filter(session=form.cleaned_data['session'])
            if form.cleaned_data.get('batch'):
                applications = applications.filter(batch=form.cleaned_data['batch'])
            if form.cleaned_data.get('department'):
                applications = applications.filter(department=form.cleaned_data['department'])
            if form.cleaned_data.get('semester'):
                semester = Semester_Status(form.cleaned_data['semester'])
                applications = applications.filter(semester=semester)
            if form.cleaned_data.get('registration_number'):
                applications = applications.filter(registration_number__icontains=form.cleaned_data['registration_number'])
            if form.cleaned_data.get('application_status'):
                application_status = Application_Status(form.cleaned_data['application_status'])
                applications = applications.filter(application_status=application_status)
    else:
        applications = DormitoryApplications.objects.filter(
                        application_status=Application_Status.Pending).all()

    context = {
        'dataset' : applications,
        'form' : form,
    }

    return render(request, 'dormitoryApplications/index.html', context)


