from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from .models import * 

def submit_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        # Save the notice to the database
        notice = Notice(title=title, description=description, date=date)
        notice.save()
        
        # Redirect to a success page or back to the Provost Notice page
        return redirect('provost_notice')
    
    # If the request method is not POST, redirect back to the Provost Notice page
    return redirect('provost_notice')

def provost_notice(request):
    return render(request, 'provost_notice.html', )


def provost_notices(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'provost_notices.html', {'notices': notices})


# views.py in your Communication app

def delete_notice(request, notice_id):
    # Retrieve the notice object
    notice = get_object_or_404(Notice, id=notice_id)
    
    if request.method == 'POST':
        # Delete the notice
        notice.delete()
        # Redirect to a success page or any other page
        return redirect('provost_notices')

    # If request method is not POST, render the notice deletion confirmation page
    return render(request, 'delete_notice_confirmation.html', {'notice': notice})


