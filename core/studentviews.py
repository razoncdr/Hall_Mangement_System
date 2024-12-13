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
from django.db import transaction
from core.utils import generate_verification_link, generate_random_password
from .models import *
from HallManagementApp.models import *
from .forms import *
from .decorators import *
import datetime
from django.db.models import Q

from django.core.mail import send_mail


@allowed_users(allowed_roles=['Admin', 'Hall Provost', 'Operator'])
def dormitoryApplication_list(request):
    applications = DormitoryApplications.objects.none()

    form = DormitoryApplicationsFilterForm(request.POST or None)    
    if request.method == "POST":
        if form.is_valid():
            applications = DormitoryApplications.objects.filter(
                            application_date__gte=form.cleaned_data['date_from'], 
                            application_date__lt=form.cleaned_data['date_to'] + datetime.timedelta(days=1),
                            is_email_verified=True).all()

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
                        application_status=Application_Status.Pending,
                        is_email_verified=True).all()

    context = {
        'dataset' : applications,
        'form' : form,
    }

    return render(request, 'dormitoryApplications/index.html', context)


def verify_email(request, uuid, token):
    dorm_application = get_object_or_404(DormitoryApplications, uuid=uuid, token=token)

    if dorm_application.is_email_verified == False:
        dorm_application.is_email_verified = True
        dorm_application.save()
        messages.success(request, 'Your email has been verified successfully!')

        # Send email
        subject = "Email Verified Successfully"
        update_url = f"http://127.0.0.1:8000/applications/{dorm_application.uuid}/{dorm_application.token}/update/"  
        message = (
            f"Hi {dorm_application.fullName},\n\n"
            "Your email has been verified successfully!\n"
            "You can update your application using the following link:\n"
            f"{update_url}\n\n"
            "Thank you for your application."
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [dorm_application.email]

        try:
            send_mail(subject, message, from_email, to_list, fail_silently=True)

        except Exception as e:
            messages.error(request, f"An error occurred while sending the email: {e}")


        return redirect('application_update', uuid=dorm_application.uuid, token=dorm_application.token)
    
    else:
        return HttpResponse('Invalid or expired verification link.', status=400)


def dormitoryApplicationCreate(request):
    message = ""

    if request.method == 'POST':

        post_data = request.POST.copy()  # Make a mutable copy of the POST data
        post_data['application_date'] = datetime.datetime.now()
        form = DormitoryApplicationsForm(post_data, request.FILES)

        if form.is_valid():
            # Create an instance of the form but don't save it yet
            if Student.objects.filter(registration_number=form.cleaned_data['registration_number']).exists():         
                messages.error(request, "A student with the registration number already exists.")

            elif DormitoryApplications.objects.filter(email=form.cleaned_data['email']).exists():         
                messages.error(request, "An application with this email address already exists.")

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
                # print(full_url)
                
                # Send email
                subject = "Verify your email"
                message = f"Hi {instance.fullName},\nPlease verify your email by clicking on the following link: {full_url}"
                from_email = settings.EMAIL_HOST_USER
                to_list = [instance.email]

                # print(message)
                # print("from: ",from_email)
                # print(to_list)
                # print(instance.email)

                try:
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.success(request, 'A verification link has been sent to your email address. Please verify your email to proceed.')
                    return redirect('application_create')
                except Exception as e:
                    instance.delete()  # Remove the instance from the database
                    messages.error(request, f"An error occurred while sending the verification email: {e}")
                    return redirect('application_create')  # Redirect back to the creation page

        else:
            errors = form.errors.as_data()
            # print(errors)           
            messages.error(request, "Form submission failed due to validation errors.")
    else:
        form = DormitoryApplicationsForm()

    context = {}
    context["message"] = message
    context["form"] = form

    return render(request, 'dormitoryApplications/create.html', context)


def update_dormitoryApplication(request, uuid, token):
    # Fetch the pending application object with matching UUID and token
    obj = get_object_or_404(
        DormitoryApplications,
        uuid=uuid,
        token=token,
        application_status=Application_Status.Pending
    )

    if request.method == 'POST':
        # Make a mutable copy of POST data and exclude the email field
        post_data = request.POST.copy()
        post_data['email'] = obj.email  # Ensure email remains unchanged
        form = DormitoryApplicationsForm(post_data, request.FILES, instance=obj)

        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']

            # Check if the registration number already belongs to a student
            if Student.objects.filter(registration_number=registration_number).exists():
                messages.error(request, "A student with this registration number already exists.")
            else:
                # Check for duplicate applications with the same registration number
                duplicate_applications = DormitoryApplications.objects.filter(
                    registration_number=registration_number,
                    application_status=Application_Status.Pending
                ).exclude(uuid=obj.uuid)

                if duplicate_applications.exists():
                    duplicate_applications.delete()  # Delete duplicate pending applications

                # Save the form instance
                instance = form.save(commit=False)
                instance.application_status = Application_Status.Pending  # Ensure status is still Pending
                instance.is_email_verified = True  # Ensure is_email_verified is True
                instance.save()

                # Send a notification email to the user
                try:
                    update_url = f"http://127.0.0.1:8000/applications/{instance.uuid}/{instance.token}/update/"  
                    subject = "Application Updated Successfully"
                    message = (
                        f"Hi {instance.fullName},\n\n"
                        "Your dormitory application has been updated successfully!\n\n"
                        "You can update your application using the following link:\n"
                        f"{update_url}\n\n"
                        "Thank you for your application.\n"
                    )
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [instance.email]

                    send_mail(subject, message, from_email, to_list, fail_silently=False)
                    messages.success(request, "Your application has been updated successfully! A confirmation email has been sent.")
                except Exception as e:
                    messages.error(request, f"An error occurred while sending the email: {e}")

                # Redirect to the same page
                return redirect('application_update', uuid=instance.uuid, token=instance.token)
        else:
            # Handle form validation errors
            messages.error(request, "Form submission failed due to validation errors.")
    else:
        # Load the form with the existing object data, excluding the email field
        form = DormitoryApplicationsForm(instance=obj)
        form.fields['email'].disabled = True  # Make the email field read-only

    # Render the update page with the form
    return render(request, 'dormitoryApplications/edit.html', {"form": form})


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

            # Send rejection email
            try:
                subject = "Dormitory Application Rejected"
                message = (
                    f"Dear {obj.fullName},\n\n"
                    f"Your dormitory application has been reviewed and unfortunately, it has been rejected.\n\n"
                    f"Remarks: {obj.remarks}\n\n"
                    f"For further details, please contact the hall office.\n\n"
                    "Thank you."
                )
                send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email], fail_silently=False)
                messages.success(request, f"The application has been rejected, and an email notification has been sent to {obj.email}.")
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")

        elif request.POST.get('status') == 'approved':
            # Approve the application and create related entities
            try:
                with transaction.atomic():
                    # Ensure atomicity
                    if User.objects.filter(username=obj.registration_number).exists():
                        error_message = f"Registration No. '{obj.registration_number}' already exists!"
                        messages.error(request, error_message)
                        raise Exception(error_message)

                    # Generate a random password
                    random_password = generate_random_password()

                    # Create user and related entities
                    user, user_profile, student = create_user_and_student(obj, random_password)

                    obj.application_status = Application_Status.Approved
                    obj.remarks = request.POST.get('remarks')
                    obj.review_date = timezone.now()
                    obj.save()

                    # Send rejection email
                    try:
                        subject = "Dormitory Application Approved"
                        message = (
                            f"Dear {obj.fullName},\n\n"
                            f"Congratulations! Your dormitory application has been approved.\n\n"
                            f"Remarks: {obj.remarks}\n\n"
                            f"Your account details:\nUsername: {user.username}\nPassword: {random_password}\n\n"
                            "Thank you."
                        )
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email], fail_silently=False)
                        messages.success(request, f"Account created for {user.username}. Student '{student.fullName}' created successfully!")
                    
                    except Exception as e:
                        messages.error(request, f"Failed to send email: {e}")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    form = DormitoryApplicationsForm(instance=obj)
    form.initial['semester'] = obj.semester.value
    form.initial['application_status'] = obj.application_status.value

    context["form"] = form
    context["data"] = obj
    return render(request, 'dormitoryApplications/review.html', context)


def create_user_and_student(application, random_password):
    """
    Create User, UserProfile, and Student entities from a dormitory application.
    """
    # Create User
    user = User.objects.create_user(
        username=application.registration_number,
        password=random_password,
        first_name=application.fullName,
        email=application.email,
        date_joined=timezone.now()
    )

    # Assign the "Student" group to the user
    group, _ = Group.objects.get_or_create(name="Student")
    user.groups.add(group)

    # Create UserProfile
    user_profile = UserProfile.objects.create(
        user=user,
        fullName=application.fullName,
        birthDate=application.birthDate,
        phone=application.phone,
        email=application.email,
        entryDate=timezone.now()
    )

    # Fetch related entities
    batch = Batch.objects.get(id=application.batch_id)
    department = Department.objects.get(id=application.department_id)
    session = Session.objects.get(id=application.session_id)

    # Create Student
    student = Student.objects.create(
        userprofile=user_profile,
        session=session,
        batch=batch,
        semester=application.semester,
        department=department,
        registration_number=application.registration_number,
        fullName=application.fullName,
        birthDate=application.birthDate,
        gender=application.gender,
        phone=application.phone,
        email=application.email,
        picture=application.picture,
        idCardPicture=application.idCardPicture,
        guardian_name=application.guardian_name,
        guardian_relation=application.guardian_relation,
        guardian_phone=application.guardian_phone,
        guardian_address=application.guardian_address,
        status="active"
    )

    return user, user_profile, student



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
    