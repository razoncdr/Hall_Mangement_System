from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import (get_object_or_404, render)

from .decorators import *
from .forms import *


#################################   CRUD Operation for Hall   ############################################


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def hall_list(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

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

    context['form'] = form

    return render(request, "hall/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def edithall(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Hall, id=id)

    # pass the object as instance in form
    form = HallForm(request.POST or None, instance=obj)

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
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Hall, id=request.POST.get("id"))

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

    context['form'] = form

    return render(request, "room/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editroom(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Room, id=id)

    # pass the object as instance in form
    form = RoomForm(request.POST or None, instance=obj)

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
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Room, id=request.POST.get("id"))

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
    context = {}

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

    context['form'] = form

    return render(request, "batch/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editbatch(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Batch, id=id)

    # pass the object as instance in form
    form = BatchForm(request.POST or None, instance=obj)

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
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Batch, id=request.POST.get("id"))

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
    context = {}

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

    context['form'] = form

    return render(request, "department/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editdepartment(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Department, id=id)

    # pass the object as instance in form
    form = DepartmentForm(request.POST or None, instance=obj)

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
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Department, id=request.POST.get("id"))

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
    context = {}

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

    context['form'] = form

    return render(request, "session/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editsession(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Session, id=id)

    # pass the object as instance in form
    form = SessionForm(request.POST or None, instance=obj)

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
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Session, id=request.POST.get("id"))

        # delete object
        obj.delete()

        # after deleting redirect to
        # home page
        return redirect("session_list")

    #################################   CRUD Operation for Semester   ############################################


#################################   CRUD Operation for Semester   ############################################

@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def semester_list(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = Semester.objects.order_by("name").all()

    return render(request, "semester/index.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_semester(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = SemesterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("semester_list")

    context['form'] = form

    return render(request, "semester/create.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def edit_semester(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Semester, id=id)

    # pass the object as instance in form
    form = SemesterForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to semesterlist
    if form.is_valid():
        form.save()
        return redirect("semester_list")

    # add form dictionary to context
    context["form"] = form

    return render(request, "semester/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def delete_semester(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Semester, id=request.POST.get("id"))

        # delete object
        obj.delete()

        # after deleting redirect to
        # home page
        return redirect("semester_list")


#################################   CRUD Operation for Student   ############################################


# @allowed_users(allowed_roles=['Admin', 'Hall Provost'])
# def create_student(request):

#     error_message = ""
#     success_message = ""
#     # Handle GET requests or render form again with initial data
#     form = StudentForm(request.POST or None)

#     if request.method == 'POST':
#         if User.objects.filter(username=request.POST.get("registration_number")).exists():
#             error_message = f"Registration No. '{request.POST.get('registration_number')}' already exists!"

#         else:
#             name = request.POST.get('name')
#             registration_number = request.POST.get('registration_number')
#             status = request.POST.get('status')
#             batch_id = request.POST.get('batch')
#             department_id = request.POST.get('department')
#             session_id = request.POST.get('session')
#             room_id = request.POST.get('room')

#             batch = Batch.objects.get(id=batch_id)
#             department = Department.objects.get(id=department_id)
#             session = Session.objects.get(id=session_id)
#             room = Room.objects.get(id=room_id)

#             # user = UserProfile.objects.create_user(username=registration_number, password=''+registration_number)
#             user = User()
#             user.first_name = name
#             user.last_name = ""
#             user.username = request.POST.get("registration_number")
#             user.email = ""
#             user.set_password(registration_number)
#             user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')

#             group_name = "Student"
#             group, created = Group.objects.get_or_create(name=group_name)

#             user.save()
#             user.groups.add(group.id)
#             # user.groups.add(Student)
#             messages.success(request, 'Account was created for ' + user.username)

#             userinfo = UserProfile(user=authenticate(request, username=user.username, password = user.password))
#             userinfo.fullName = name
#             userinfo.user = user
#             userinfo.entryDate = datetime.datetime.now().strftime('%Y-%m-%d')
#             userinfo.save()

#             student = Student.objects.create(
#                 name=name,
#                 registration_number=registration_number,
#                 batch=batch,
#                 department=department,
#                 session=session,
#                 room = room, 
#                 userprofile = userinfo, 
#                 status = status, 
#             )

#             # Redirect or render a success page
#             success_message = f"Student '{student.name}' created successfully!"

#     return render(request, 'student/create.html', {'form': form, 'error_message': error_message, 'success_message': success_message})


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def create_student(request):
    error_message = ""
    success_message = ""
    form = StudentForm(request.POST or None)

    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get("registration_number")).exists():
            error_message = f"Registration No. '{request.POST.get('registration_number')}' already exists!"
        else:
            name = request.POST.get('fullName')
            if not name:
                error_message = "The full name cannot be empty."
                return render(request, 'student/create.html', {'form': form, 'error_message': error_message})

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

            user = User()
            user.first_name = name
            user.last_name = ""
            user.username = registration_number
            user.email = ""
            user.set_password(registration_number)
            user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')

            group_name = "Student"
            group, created = Group.objects.get_or_create(name=group_name)

            user.save()
            user.groups.add(group.id)

            userinfo = UserProfile(user=user)
            userinfo.fullName = name
            userinfo.entryDate = datetime.datetime.now().strftime('%Y-%m-%d')
            userinfo.save()

            student = Student.objects.create(
                fullName=name,
                registration_number=registration_number,
                batch=batch,
                department=department,
                session=session,
                room=room,
                userprofile=userinfo,
                status=status,
            )

            success_message = f"Student '{student.fullName}' created successfully!"

    return render(request, 'student/create.html',
                  {'form': form, 'error_message': error_message, 'success_message': success_message})


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def editstudent(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Student, id=id)

    # pass the object as instance in form
    form = StudentForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to student_list
    if form.is_valid():
        if User.objects.filter(username=request.POST.get("registration_number")).exists():
            messages.warning(request, f"Registration No. '{request.POST.get('registration_number')}' already exists!")
        else:
            form.save()
            messages.success(request, "Save Successful!!")

    # add form dictionary to context
    context["form"] = form

    return render(request, "student/edit.html", context)


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def deletestudent(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(Student, id=request.POST.get("id"))

        # delete object
        obj.delete()

        # after deleting redirect to
        # home page
        return redirect("student_list")


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def student_list(request):
    students = Student.objects.none()

    form = StudentFilterForm(request.POST or None)
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        students = Student.objects.order_by('registration_number').all()
        if request.POST.get("hall") != "":
            print("hallid: " + request.POST.get("hall"))
            students = students.filter(room__hall_id=request.POST.get("hall"))

        if request.POST.get("room") != "":
            print("roomid: " + request.POST.get("room"))
            students = students.filter(room__name__icontains=request.POST.get("room"))

        if request.POST.get("batch") != "":
            print(request.POST.get("batch"))
            students = students.filter(batch_id=request.POST.get("batch"))

        # if request.POST.get("semester") != "":
        #     print(request.POST.get("hall")) 
        #     studentfees = studentfees.filter(student__room__hall_id=request.POST.get("hall"))

        if request.POST.get("registration_number") != "":
            print(request.POST.get("registration_number"))
            students = students.filter(registration_number__icontains=request.POST.get("registration_number"))
        if request.POST.get("status") != "":
            print(request.POST.get("status"))
            students = students.filter(status=request.POST.get("status"))

    context = {
        'students': students,
        'form': form,
    }
    return render(request, 'student/index.html', context)


# Student Fees Module

@allowed_users(allowed_roles=['Hall Provost', 'Admin'])
def feesheadlist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()

    return render(request, "feeshead/index.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'operator'])
def createfeeshead(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = FeesHeadForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("feeshead_list")

    context['form'] = form

    return render(request, "feeshead/create.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'operator'])
def editfeeshead(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(FeesHead, id=id)

    # pass the object as instance in form
    form = FeesHeadForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to feeshead_list
    if form.is_valid():
        form.save()
        return redirect("feeshead_list")

    # add form dictionary to context
    context["form"] = form

    return render(request, "feeshead/edit.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'operator'])
def deletefeeshead(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(FeesHead, id=request.POST.get("id"))

        # delete object
        obj.delete()

        # after deleting redirect to
        # home page
        return redirect("feeshead_list")


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def generatestudentfee(request):
    # dictionary for initial data with

    context = {}
    form = StudentFeeForm(request.POST or None)

    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        students = Student.objects.filter(status='active')

        if request.POST.get("session") != "":
            # print(request.POST.get("batch"))
            students = students.filter(session=request.POST.get("session"))

        if request.POST.get("batch") != "":
            # print(request.POST.get("batch"))
            students = students.filter(batch=request.POST.get("batch"))

        if request.POST.get("registration_number") != "":
            # print(request.POST.get("registration_number"))
            students = students.filter(registration_number=request.POST.get("registration_number"))

        semester = Semester.objects.get(id=request.POST.get("semester"))
        feeshead = FeesHead.objects.get(id=request.POST.get("feesHead"))
        # print(students)
        for student in students:
            student.semesterid = semester.id
            student.semester = semester.name
            student.feesheadid = feeshead.id
            student.fee_title = feeshead.title
            student.amount = feeshead.amount
            student.isgenerated = StudentFees.objects.filter(student=student,
                                                             semester=semester, feeshead=feeshead).exists()
            if student.isgenerated:
                student.bgcolor = "bg-secondary text-white"
                student.fee_status = StudentFees.objects.filter(student=student,
                                                                semester=semester,
                                                                feeshead=feeshead).first().paymentStatus.name
            else:
                student.fee_status = Payment_Status.UNPAID.name

        context['dataset'] = students

    context['form'] = form

    return render(request, "studentfee/create.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def createstudentfee(request):
    # dictionary for initial data with
    try:
        context = {}
        if request.method == "POST":
            # form = CreateUserForm(request.POST)
            # if request.method.is_valid():
            # data = request.POST.getlist("studentfees[]")
            # print(data)

            # studentfee = json.loads(studentfee)
            # print(studentfee)
            studentFeeInfo = StudentFees()
            studentFeeInfo.student = Student.objects.get(id=request.POST.get("studentid"))
            studentFeeInfo.feeshead = FeesHead.objects.get(id=request.POST.get("feesheadid"))
            studentFeeInfo.semester = Semester.objects.get(id=request.POST.get("semesterid"))
            studentFeeInfo.amount = request.POST.get("amount")
            studentFeeInfo.paymentStatus = Payment_Status.UNPAID
            studentFeeInfo.entryuser = UserProfile.objects.get(user=request.user)
            studentFeeInfo.entryDate = datetime.datetime.now()
            studentFeeInfo.save()

        # return render(request, "studentfee/create.html", context)
        return JsonResponse({"success": True}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "message": e}, status=400)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def studentfeelist(request):
    studentfees = StudentFees.objects.none()
    # batches = Batch.objects.all()  # Assuming you have a Batch model
    # halls = Hall.objects.all()  # Assuming you have a Hall model    
    # feesHeads = FeesHead.objects.all()  # Assuming you have a Hall model

    form = StudentFeeFilterForm(request.POST or None)

    if request.method == "POST":

        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():

        ToDate = datetime.datetime.strptime(request.POST.get("To_Date"), "%Y-%m-%d") + datetime.timedelta(days=1)
        FromDate = datetime.datetime.strptime(request.POST.get("From_Date"), "%Y-%m-%d")

        studentfees = StudentFees.objects.filter(entryDate__gte=FromDate,
                                                 entryDate__lt=ToDate, ).order_by('-entryDate').all()
        if request.POST.get("feesHead") != "":
            # print("feesHeadid: " + request.POST.get("feesHead")) 
            studentfees = studentfees.filter(feeshead=request.POST.get("feesHead"))

        if request.POST.get("batch") != "":
            # print("batchid: " + request.POST.get("batch")) 
            studentfees = studentfees.filter(student__batch_id=request.POST.get("batch"))

        # if request.POST.get("hall") != "":
        #     print("hallid: " + request.POST.get("hall")) 
        #     studentfees = studentfees.filter(student__room__hall_id=request.POST.get("hall"))

        if request.POST.get("semester") != "":
            # print("semesterid: " + request.POST.get("semester")) 
            studentfees = studentfees.filter(semester_id=request.POST.get("semester"))

        if request.POST.get("registration_number") != "":
            # print(request.POST.get("registration_number")) 
            studentfees = studentfees.filter(student__registration_number=request.POST.get("registration_number"))

        if request.POST.get("payment_Status") != "":
            # print(request.POST.get("payment_Status")) 
            payment_Status = Payment_Status(request.POST.get("payment_Status"))
            # print(payment_Status)
            studentfees = studentfees.filter(paymentStatus=payment_Status)

    context = {
        'studentfees': studentfees,
        'form': form,
    }
    return render(request, 'studentfee/index.html', context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'Operator'])
def deletestudentfee(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == "POST":
        # fetch the object related to passed id
        obj = get_object_or_404(StudentFees, id=request.POST.get("id"))

        # delete object
        obj.delete()

        # after deleting redirect to
        # home page
        return redirect("studentfeelist")


# edit by : Rejwanul Haque 

@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def dining_managers(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()

    return render(request, "feeshead/index.html", context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def members(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = FeesHead.objects.all()

    return render(request, "feeshead/index.html", context)
