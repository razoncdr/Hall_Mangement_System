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
from core.decorators import *
from core.forms import *
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)

def create_student(request):
    success_message = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        batch_id = request.POST.get('batch')
        department_id = request.POST.get('department')
        session_id = request.POST.get('session')
        
        batch = Batch.objects.get(id=batch_id)
        department = Department.objects.get(id=department_id)
        session = Session.objects.get(id=session_id)
        
        student = Student.objects.create(
            name=name,
            registration_number=registration_number,
            batch=batch,
            department=department,
            session=session
        )
        # Redirect or render a success page
        success_message = f"Student '{student.name}' created successfully!"

        
    # Handle GET requests or render form again with initial data
    batches = Batch.objects.all()
    departments = Department.objects.all()
    sessions = Session.objects.all()
    form = StudentForm()
    return render(request, 'student_form.html', {
                    'batches': batches
                     , 'departments': departments
                     , 'sessions': sessions
                     , 'form': form
                     , 'success_message': success_message})



@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def editstudent(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    
    # fetch the object related to passed id
    obj = get_object_or_404(Student, id = id)
 
    # pass the object as instance in form
    form = StudentForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to student_list
    if form.is_valid():
        form.save()
        return redirect("student_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "studentedit.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'operator'])
def deletestudent(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Student, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("student_list")
    

def student_list(request):
    students = Student.objects.all().order_by('registration_number')
    return render(request, 'studentList1.html', {'students': students})