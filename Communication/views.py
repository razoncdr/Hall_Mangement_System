from core.decorators import allowed_users
from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from .models import * 

@allowed_users(allowed_roles=['Hall Provost', 'Developer'])
def submit_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        # Save the notice to the database
        notice = Notice(title=title, description=description, date=date)
        notice.save()
        
        # Redirect to a success page or back to the Provost Notice page
        return redirect('provost_notices')
    
    # If the request method is not POST, redirect back to the Provost Notice page
    return redirect('provost_notice')

@allowed_users(allowed_roles=['Student', 'Developer'])
def submit_student_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        # Save the notice to the database
        notice = StudentNotice(title=title, description=description, date=date)
        notice.save()
        
        # Redirect to a success page or back to the Provost Notice page
        return redirect('student_messages')
    
    # If the request method is not POST, redirect back to the Provost Notice page
    return redirect('student_notice')

@allowed_users(allowed_roles=['Hall Provost'])
def provost_notice(request):
    return render(request, 'communication/provost_notice.html', )

@allowed_users(allowed_roles=['Student', 'Developer'])
def student_notice(request):
    if request.method == 'POST':
        form = StudentNotice(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user.student  # Assuming each student has a one-to-one relationship with a User
            application.save()
            return redirect('application_detail', pk=application.pk)
    else:
        form = StudentNotice()
    return render(request, 'communication/student_notice.html', {'notice': form})

@allowed_users(allowed_roles=['Hall Provost', 'Student'])
def student_messages(request):
    notices = StudentNotice.objects.all().order_by('-date')
    return render(request, 'communication/student_messages.html', {'notices': notices})


@allowed_users(allowed_roles=['Hall Provost', 'Student'])
def provost_notices(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'communication/provost_notices.html', {'notices': notices})


# views.py in your Communication app

@allowed_users(allowed_roles=['Hall Provost', 'Developer'])
def delete_notice(request, notice_id):
    # Retrieve the notice object
    notice = get_object_or_404(Notice, id=notice_id)
    
    if request.method == 'POST':
        # Delete the notice
        notice.delete()
        # Redirect to a success page or any other page
        return redirect('provost_notices')

    # If request method is not POST, render the notice deletion confirmation page
    return render(request, 'communication/delete_notice_confirmation.html', {'notice': notice})

@allowed_users(allowed_roles=['Student', 'Developer'])
def delete_student_notice(request, notice_id):
    # Retrieve the notice object
    notice = get_object_or_404(StudentNotice, id=notice_id)
    
    if request.method == 'POST':
        # Delete the notice
        notice.delete()
        # Redirect to a success page or any other page
        return redirect('student_messages')

    # If request method is not POST, render the notice deletion confirmation page
    return render(request, 'communication/delete_notice_confirmation.html', {'notice': notice})


