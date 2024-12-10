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

from core.utils import generate_verification_link
from .models import *
from HallManagementApp.models import *
from .forms import *
from .decorators import *
import datetime
from django.db.models import Q


from django.core.mail import send_mail


@allowed_users(allowed_roles=['Admin', 'Hall Provost'])
def dormitoryApplication_list(request):
    applications = DormitoryApplications.objects.none()

    form = DormitoryApplicationsFilterForm(request.POST or None)    
    if request.method == "POST":
        if form.is_valid():
            applications = DormitoryApplications.objects.filter(
                            application_date__gte=form.cleaned_data['date_from'], 
                            application_date__lt=form.cleaned_data['date_to']+ datetime.timedelta(days=1)).all()

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




from django.utils.timezone import now

def verify_email(request, uuid, token):
    dorm_application = get_object_or_404(DormitoryApplications, uuid=uuid)
    token_expiry_time = datetime.timedelta(days=1)  # Example: 1-day expiration

    if dorm_application.token == token and now() - dorm_application.application_date <= token_expiry_time:
        dorm_application.is_email_verified = True
        dorm_application.save()
        messages.success(request, 'Your email has been verified successfully!')
        return redirect('application_update', uuid=dorm_application.uuid, token=dorm_application.token)
    else:
        return HttpResponse('Invalid or expired verification link.', status=400)




def dormitoryApplicationCreate(request):
    message = ""
    if request.method == 'POST':

        post_data = request.POST.copy()  # Make a mutable copy of the POST data
        post_data['application_date'] = datetime.datetime.now()
        form = DormitoryApplicationsForm(post_data, request.FILES)

        # print(form)
        if form.is_valid():
            # Create an instance of the form but don't save it yet
            if Student.objects.filter(registration_number=form.cleaned_data['registration_number']).exists():         
                messages.error(request, "A student with the registration number already exists.")

            else:
                if DormitoryApplications.objects.filter(registration_number=form.cleaned_data['registration_number'],
                                                       application_status=Application_Status.Pending).exists(): 
                    dormApplication = DormitoryApplications.objects.get(registration_number=form.cleaned_data['registration_number'],
                                                        application_status=Application_Status.Pending)
                    dormApplication.delete()

                instance = form.save(commit=False)
                instance.application_status = Application_Status.Pending
                instance.application_date = datetime.datetime.now()
                instance.save()

                

                # Generate verification link
                verification_url = generate_verification_link(instance)
                full_url = f"http://127.0.0.1:8000{verification_url}"
                print(full_url)
                
                # Send email
                subject = "Verify your email"
                message = f"Hi {instance.fullName},\nPlease verify your email by clicking on the following link: {full_url}"
                from_email = settings.EMAIL_HOST_USER
                to_list = [instance.email]


                print(message)
                print("from: ",from_email)
                print(to_list)
                print(instance.email)
                
                try:
                    send_mail(subject, message, from_email, to_list, fail_silently=False)
                    print("Email sent successfully")
                except Exception as e:
                    instance.delete()  # Remove the instance from the database
                    messages.error(request, f"An error occurred while sending the verification email: {e}")

                    print(f"Error sending email: {e}")
                    return redirect('application_create')  # Redirect back to the creation page

                # messages.success(request, 'Registration successful! Please check your email to verify your account.')
                # return redirect('login')



                messages.success(request, 'Form Submitted Successfully!!')
                return redirect('application_create')

        else:
            errors = form.errors.as_data()
            print(errors)           
            messages.error(request, "Form submission failed due to validation errors.")
    else:
        form = DormitoryApplicationsForm()

    context = {}
    context["message"] = message
    context["form"] = form

    return render(request, 'dormitoryApplications/create.html', context)




def update_dormitoryApplication(request, uuid, token):
    
    obj = get_object_or_404(DormitoryApplications, uuid=uuid, token=token)

    context = {}
    
    if request.method == 'POST':

        post_data = request.POST.copy()  # Make a mutable copy of the POST data
        post_data['application_date'] = datetime.datetime.now()
        form = DormitoryApplicationsForm(post_data, request.FILES, instance=obj)

        if form.is_valid():
            # Create an instance of the form but don't save it yet
            if Student.objects.filter(registration_number=form.cleaned_data['registration_number']).exists():         
                messages.error(request, "A student with the registration number already exists.")
   
            else:
                if DormitoryApplications.objects.filter(registration_number=form.cleaned_data['registration_number'],
                                                       application_status=Application_Status.Pending).exists(): 
                    dormApplication = DormitoryApplications.objects.get(registration_number=form.cleaned_data['registration_number'],
                                                        application_status=Application_Status.Pending)
                    dormApplication.delete()

                instance = form.save(commit=False)
                instance.application_status = Application_Status.Pending
                instance.application_date = datetime.datetime.now()
                instance.save()

                messages.success(request, 'Form Submitted Successfully!!')
                return redirect('application_update', uuid=instance.uuid, token=instance.token)

        else:
            # Form is invalid, handle the validation errors
            errors = form.errors.as_data()
            # You can print errors to debug or log them
            # print(errors)
            # In a real application, you might want to do something more user-friendly
            # For simplicity, we'll just update the message to indicate validation errors            
            messages.error(request, "Form submission failed due to validation errors.")
    
    else:
        form = DormitoryApplicationsForm(instance = obj)
        
    context["form"] = form

    return render(request, 'dormitoryApplications/edit.html', context)


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'Operator'])
def review_dormitoryApplication(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    
    # fetch the object related to passed id
    obj = get_object_or_404(DormitoryApplications, id = id)

    if request.method == 'POST':
        # print(request.POST.get('status') )
        if request.POST.get('status') == 'rejected':
            obj.application_status = Application_Status.Rejected
            obj.remarks = request.POST.get('remarks')
            obj.review_date = datetime.datetime.now()
            obj.save()

        else:
            if User.objects.filter(username=obj.registration_number).exists():
                error_message = f"Registration No. '{obj.registration_number}' already exists!"
                messages.error(request, f"Registration No. '{obj.registration_number}' already exists!")

            else:
                fullName = obj.fullName
                registration_number = obj.registration_number
                status = 'active'
                batch_id = obj.batch_id
                department_id = obj.department_id
                session_id = obj.session_id
                
                batch = Batch.objects.get(id=batch_id)
                department = Department.objects.get(id=department_id)
                session = Session.objects.get(id=session_id)
                
                # user = UserProfile.objects.create_user(username=registration_number, password=''+registration_number)
                user = User()
                user.first_name = fullName
                user.last_name = ""
                user.username = registration_number
                user.email = obj.email
                user.set_password(registration_number)
                user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')

                group_name = "Student"
                group, created = Group.objects.get_or_create(name=group_name)

                user.save()
                user.groups.add(group.id)
                # user.groups.add(Student)

                userinfo = UserProfile(user=authenticate(request, username=user.username, password = user.password))
                userinfo.fullName = fullName
                userinfo.birthDate = obj.birthDate
                userinfo.phone = obj.phone
                userinfo.email = obj.email
                userinfo.user = user
                userinfo.entryDate = datetime.datetime.now().strftime('%Y-%m-%d')
                userinfo.save()

                student = Student.objects.create(
                    # room = NULL, 
                    userprofile = userinfo, 
                    
                    session = session,
                    batch = batch,
                    semester = obj.semester,
                    department = department,

                    registration_number=registration_number,
                    fullName=fullName,
                    birthDate=obj.birthDate,
                    gender=obj.gender,
                    phone=obj.phone,
                    email=obj.email,
                    picture=obj.picture,
                    idCardPicture=obj.idCardPicture,

                    guardian_name=obj.guardian_name,
                    guardian_relation=obj.guardian_relation,
                    guardian_phone=obj.guardian_phone,
                    guardian_address=obj.guardian_address,

                    status = status, 
                )

                # Redirect or render a success page
                messages.success(request, 'Account was created for ' + user.username + f". Student '{student.fullName}' created successfully!")
          
                obj.application_status = Application_Status.Approved
                obj.remarks = request.POST.get('remarks')
                obj.review_date = datetime.datetime.now()
                obj.save()

    # pass the object as instance in form
    form = DormitoryApplicationsForm(instance = obj)
    form.initial['semester'] = obj.semester.value
    form.initial['application_status'] = obj.application_status.value

    # add form dictionary to context
    context["form"] = form
    context["data"] = obj

    return render(request, 'dormitoryApplications/review.html', context)
    
 

@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'Operator'])
def delete_dormitoryApplication(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.method =="POST":
        # fetch the object related to passed id
        obj = get_object_or_404(DormitoryApplications, id = request.POST.get("id"))
        
        if obj.application_status != Application_Status.Approved:
            # delete object
            obj.delete()
        
        # after deleting redirect to
        # home page
        return redirect("application_list")
    