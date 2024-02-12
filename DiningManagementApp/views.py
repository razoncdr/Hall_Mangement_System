from .models import Member, DiningManager
from django.shortcuts import render, redirect
from .forms import DiningManagerForm, MemberForm

def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def dining_manager_list(request):
    dining_managers = DiningManager.objects.all()
    return render(request, 'dining_manager_list.html', {'dining_managers': dining_managers})


def add_dining_manager(request):
    if request.method == 'POST':
        form = DiningManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dining_manager_list')  # Redirect to the list of dining managers
    else:
        form = DiningManagerForm()
    return render(request, 'add_dining_manager.html', {'form': form})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')  # Redirect to the list of members
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})