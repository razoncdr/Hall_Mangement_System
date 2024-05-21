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


@allowed_users(allowed_roles=['Hall Provost', ])
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
def generatestudentfee(request):
    # dictionary for initial data with

    context = {}
    form = StudentFeeForm(request.POST or None)

    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        students = Student.objects.filter(status='active')
                       
        if request.POST.get("batch") != "":
            #print(request.POST.get("batch")) 
            students = students.filter(batch=request.POST.get("batch"))

        if request.POST.get("registration_number") != "":
            #print(request.POST.get("registration_number")) 
            students = students.filter(registration_number=request.POST.get("registration_number"))

        semester = Semester.objects.get(id = request.POST.get("semester"))
        feeshead = FeesHead.objects.get(id = request.POST.get("feesHead"))
        # print(students)
        for student in students:
            student.semesterid = semester.id
            student.semester = semester.name
            student.feesheadid = feeshead.id
            student.fee_title = feeshead.title
            student.amount = feeshead.amount
            student.isgenerated = StudentFees.objects.filter(student = student, 
                                                             semester = semester, feeshead = feeshead).exists()
            if student.isgenerated :
                student.bgcolor = "bg-secondary text-white"
                student.fee_status = StudentFees.objects.filter(student = student, 
                                semester = semester, feeshead = feeshead).first().paymentStatus.name
            else :
                student.fee_status = Payment_Status.UNPAID.name

        context['dataset'] = students
         
    context['form']= form
         
    return render(request, "studentfee/create.html", context)
    

@allowed_users(allowed_roles=['Hall Provost'])
def createstudentfee(request):
    # dictionary for initial data with
    try:
        context = {}
        if request.method == "POST":
            # form = CreateUserForm(request.POST)
            # if request.method.is_valid():
            # data = request.POST.getlist("studentfees[]")
            # print(data)

            #studentfee = json.loads(studentfee)
            #print(studentfee)
            studentFeeInfo = StudentFees()
            studentFeeInfo.student = Student.objects.get(id=request.POST.get("studentid"))
            studentFeeInfo.feeshead = FeesHead.objects.get(id=request.POST.get("feesheadid"))
            studentFeeInfo.semester = Semester.objects.get(id=request.POST.get("semesterid"))
            studentFeeInfo.amount = request.POST.get("amount")
            studentFeeInfo.paymentStatus = Payment_Status.UNPAID
            studentFeeInfo.entryuser = UserProfile.objects.get(user=request.user)
            studentFeeInfo.entryDate = datetime.datetime.now()
            studentFeeInfo.save()
            
        #return render(request, "studentfee/create.html", context)
        return JsonResponse({"success": True}, status=200)
    
    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "message": e}, status=400)
    

@allowed_users(allowed_roles=['Hall Provost'])
def studentfeelist(request):
    studentfees = StudentFees.objects.none()
    batches = Batch.objects.all()  # Assuming you have a Batch model
    halls = Hall.objects.all()  # Assuming you have a Hall model    
    feesHeads = FeesHead.objects.all()  # Assuming you have a Hall model

    form = StudentFeeFilterForm(request.POST or None)
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        studentfees = StudentFees.objects.order_by('-entryDate').all()
        if request.POST.get("feesHead") != "":
            print("feesHeadid: " + request.POST.get("feesHead")) 
            studentfees = studentfees.filter(feeshead=request.POST.get("feesHead"))
            
        if request.POST.get("batch") != "":
            print("batchid: " + request.POST.get("batch")) 
            studentfees = studentfees.filter(student__batch_id=request.POST.get("batch"))

            
        if request.POST.get("hall") != "":
            print("hallid: " + request.POST.get("hall")) 
            studentfees = studentfees.filter(student__room__hall_id=request.POST.get("hall"))

        if request.POST.get("semester") != "":
            print("semesterid: " + request.POST.get("semester")) 
            studentfees = studentfees.filter(semester_id=request.POST.get("semester"))

        if request.POST.get("registration_number") != "":
            print(request.POST.get("registration_number")) 
            studentfees = studentfees.filter(student__registration_number=request.POST.get("registration_number"))


    context = {
        'studentfees': studentfees,
        'batches': batches,
        'halls': halls,
        'feesHeads': feesHeads,
        'form': form,
    }
    return render(request, 'studentfee/index.html', context)


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def deletestudentfee(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(StudentFees, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("studentfeelist")
    


# edit by : Rejwanul Haque 

@allowed_users(allowed_roles=['Hall Provost', ])
def dining_managers(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()
         
    return render(request, "feeshead/index.html", context)



@allowed_users(allowed_roles=['Hall Provost', ])
def members(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()
         
    return render(request, "feeshead/index.html", context)