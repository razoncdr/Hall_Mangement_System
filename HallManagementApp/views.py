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
from core.decorators import *
from core.forms import *
from HallManagementApp.forms import *
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.db.models import Q



#################################   CRUD Operation for Hall   ############################################




@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def hall_list(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    halls = Hall.objects.all()

    form = HallListFilterForm(request.POST or None)
    if request.method == "POST":
            
        # if request.POST.get("hall") != "":
        #     print(request.POST.get("hall")) 
        halls = halls.filter(id=request.POST.get("hall"))

    # add the dictionary during initialization
    # context["dataset"] = Hall.objects.all()
    print(len(halls))
    for hall in halls:
        print(hall.name)
    context["halls"] = halls
    context["form"] = form
         
    return render(request, "hall/index.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_hall(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = HallForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("hall_list")
        
         
    context['form']= form
         
    return render(request, "hall/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def edithall(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Hall, id = id)
 
    # pass the object as instance in form
    form = HallForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to halllist
    if form.is_valid():
        form.save()
        return redirect("hall_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "hall/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deletehall(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Hall, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("hall_list")
 


#################################   CRUD Operation for Room   ############################################


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def room_list(request):
    context = {}
    rooms = Room.objects.all()
    halls = Hall.objects.all()
    form = RoomListFilterForm(request.POST or None)

    if request.POST.get("hall"):
        rooms = rooms.filter(hall_id=request.POST.get("hall"))
    
    search_term = request.POST.get("room")
    if search_term:
        rooms = rooms.filter(Q(name__startswith=search_term))

    context["rooms"] = rooms
    context["halls"] = halls
    context["form"] = form
       
    return render(request, "room/index.html", context)




@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_room(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("room_list")
        
         
    context['form']= form
         
    return render(request, "room/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editroom(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Room, id = id)
 
    # pass the object as instance in form
    form = RoomForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to roomlist
    if form.is_valid():
        form.save()
        return redirect("room_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "room/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deleteroom(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Room, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("room_list")
 

#################################   CRUD Operation for Batch   ############################################



@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def batch_list(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Batch.objects.order_by("-name").all()
         
    return render(request, "batch/index.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_batch(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = BatchForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("batch_list")
        
         
    context['form']= form
         
    return render(request, "batch/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editbatch(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Batch, id = id)
 
    # pass the object as instance in form
    form = BatchForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to batchlist
    if form.is_valid():
        form.save()
        return redirect("batch_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "batch/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deletebatch(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Batch, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("batch_list")
 




#################################   CRUD Operation for Department   ############################################



@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def department_list(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Department.objects.order_by("name").all()
         
    return render(request, "department/index.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_department(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("department_list")
        
         
    context['form']= form
         
    return render(request, "department/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editdepartment(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Department, id = id)
 
    # pass the object as instance in form
    form = DepartmentForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to departmentlist
    if form.is_valid():
        form.save()
        return redirect("department_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "department/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deletedepartment(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Department, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("department_list")
 





#################################   CRUD Operation for Session   ############################################



@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def session_list(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Session.objects.order_by("name").all()
         
    return render(request, "session/index.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_session(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = SessionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("session_list")
        
         
    context['form']= form
         
    return render(request, "session/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editsession(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Session, id = id)
 
    # pass the object as instance in form
    form = SessionForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to sessionlist
    if form.is_valid():
        form.save()
        return redirect("session_list")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "session/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deletesession(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Session, id = request.POST.get("id"))
        
        # delete object
        obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("session_list")
 




#################################   CRUD Operation for Student   ############################################



@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_student(request):
    success_message = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        status = request.POST.get('status')
        batch_id = request.POST.get('batch')
        department_id = request.POST.get('department')
        session_id = request.POST.get('session')
        room_id = request.POST.get('room')
        
        batch = Batch.objects.get(id=batch_id)
        department = Department.objects.get(id=department_id)
        session = Session.objects.get(id=session_id)
        room = Room.objects.get(id=room_id)
        
        # user = UserProfile.objects.create_user(username=registration_number, password=''+registration_number)
        user = User()
        user.first_name = name
        user.last_name = ""
        user.username = request.POST.get("registration_number")
        user.email = ""
        user.set_password(registration_number)
        user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')

        group_name = "Student"
        group, created = Group.objects.get_or_create(name=group_name)



        user.save()
        user.groups.add(group.id)
        # user.groups.add(Student)
        messages.success(request, 'Account was created for ' + user.username)

        userinfo = UserProfile(user=authenticate(request, username=user.username, password = user.password))
        userinfo.fullName = name
        userinfo.user = user
        userinfo.entryDate = datetime.datetime.now().strftime('%Y-%m-%d')
        userinfo.save()


        student = Student.objects.create(
            name=name,
            registration_number=registration_number,
            batch=batch,
            department=department,
            session=session,
            room = room, 
            userprofile = userinfo, 
            status = status, 
        )
        # Redirect or render a success page
        success_message = f"Student '{student.name}' created successfully!"



        
    # Handle GET requests or render form again with initial data
    batches = Batch.objects.all()
    rooms = Room.objects.all()
    departments = Department.objects.all()
    sessions = Session.objects.all()
    form = StudentForm()
    return render(request, 'student_form.html', {
                       'batches': batches
                     , 'rooms': rooms
                     , 'departments': departments
                     , 'sessions': sessions
                     , 'form': form
                     , 'success_message': success_message})


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
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


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
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
    

@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def student_list(request):
    students = Student.objects.all().order_by('batch')
    batches = Batch.objects.all()  # Assuming you have a Batch model
    halls = Hall.objects.all()  # Assuming you have a Hall model

    
    # # Searching by hall name
    # search_hall_name = request.GET.get('search_hall_name')
    # if search_hall_name:
    #     students = students.filter(room__hall__name__icontains = search_hall_name)


    # # Searching by batch
    # search_batch = request.GET.get('search_batch')
    # if search_batch:
    #     students = students.filter(batch__name__icontains=search_batch)
    
    # # Searching by room number
    # search_room_number = request.GET.get('search_room_number')
    # if search_room_number:
    #     students = students.filter(room__name__icontains=search_room_number)
    
    form = StudentFeeFilterForm(request.POST or None)
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():

        if request.POST.get("feesHead") != "":
            print(request.POST.get("feesHead")) 
            studentfees = studentfees.filter(feeshead=request.POST.get("feesHead")) 
            
        if request.POST.get("batch") != "":
            print(request.POST.get("batch")) 
            studentfees = studentfees.filter(student__batch_id=request.POST.get("batch"))

            
        if request.POST.get("hall") != "":
            print(request.POST.get("hall")) 
            studentfees = studentfees.filter(student__room__hall_id=request.POST.get("hall"))

        if request.POST.get("registration_number") != "":
            print(request.POST.get("registration_number")) 
            studentfees = studentfees.filter(student__registration_number=request.POST.get("registration_number"))



    context = {
        'students': students,
        'batches': batches,
        'halls': halls,
    }
    return render(request, 'studentList1.html', context)