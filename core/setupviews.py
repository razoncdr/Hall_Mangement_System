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
from CalculatorApp.models import *
from .forms import *
from .decorators import *
import datetime
import random
import string
import json


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def feesheadlist(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()
         
    return render(request, "feeshead/index.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def createfeeshead(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = FeesHeadForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("feeshead_list")
        
         
    context['form']= form
         
    return render(request, "feeshead/create.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def editfeeshead(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    
    # fetch the object related to passed id
    obj = get_object_or_404(FeesHead, id = id)
 
    # pass the object as instance in form
    form = FeesHeadForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to feeshead_list
    if form.is_valid():
        form.save()
        return redirect("feeshead_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "feeshead/edit.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def deletefeeshead(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(FeesHead, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("feeshead_list")
    
    
    
@allowed_users(allowed_roles=['Hall Provost'])
def createstudentfee(request):
    # dictionary for initial data with

    context = {}
    form = StudentFeeForm(request.POST or None)

    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        students = Student.objects.filter(status='active')
                       
        if request.POST.get("batch") != "":
            print(request.POST.get("batch")) 
            students = students.filter(batch=request.POST.get("batch"))

        if request.POST.get("registration_number") != "":
            print(request.POST.get("registration_number")) 
            students = students.filter(registration_number=request.POST.get("registration_number"))

        feeshead = FeesHead.objects.get(id = request.POST.get("feesHead"))
        # print(students)
        for student in students:
            student.amount = feeshead.amount

        context['dataset'] = students
         
    context['form']= form
         
    return render(request, "studentfee/create.html", context)
    