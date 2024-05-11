from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from .models import *
from .forms import *
from .decorators import *
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from .models import *
from .forms import *
from .decorators import *
import datetime

# Create your views here.

def DynamicPage(request, id):
    return HttpResponse(id)

def home(request):
    return render(request, 'home/index.html',{

    })

# def about(request):
#     return render(request, 'home/about.html',{
        
#     })

@unauthenticated_user
def loginpage(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password = request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password Incorrect')

    context = {'form': form}
    return render(request, 'accounts/login.html', context)




@allowed_users(allowed_roles=['Hall Provost', ])
def registerpage(request):
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        if request.POST.get("password1") != request.POST.get("password2"):
            messages.error(request, "Password and Confirm Password didn't match")
            usergroup = UserGroupForm()
            usergroup.user.first_name = request.POST.get("first_name")
            usergroup.user.last_name = request.POST.get("last_name")
            usergroup.user.username = request.POST.get("username")
            usergroup.user.email = request.POST.get("email")
            usergroup.group = request.POST.get("group")
            
            context = {'groups': Group.objects.all(), 'user': usergroup}
            return render(request, 'accounts/register.html', context)
            
        if User.objects.filter(username = request.POST.get("username")).exists():
            messages.error(request, "username already exist")
            usergroup = UserGroupForm()
            usergroup.user.first_name = request.POST.get("first_name")
            usergroup.user.last_name = request.POST.get("last_name")
            usergroup.user.username = request.POST.get("username")
            usergroup.user.email = request.POST.get("email")
            usergroup.group = request.POST.get("group")
            
            context = {'groups': Group.objects.all(), 'user': usergroup}
            return render(request, 'accounts/register.html', context)
            
        user = User()
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.set_password(request.POST.get("password1"))
        user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')

        group_name = request.POST.get("group")
        group, created = Group.objects.get_or_create(name=group_name)



        user.save()
        # user.groups.add("group")
        user.groups.add(request.POST.get("group"))
        messages.success(request, 'Account was created for ' + user.username)

        userinfo = UserProfile(user=authenticate(request, username=user.username, password = user.password))
        userinfo.fullName = user.first_name + " " + user.last_name
        userinfo.user = user
        userinfo.entryDate = datetime.datetime.now().strftime('%Y-%m-%d')
        userinfo.save()
    
    context = {'groups': Group.objects.all()}
    return render(request, 'accounts/register.html', context)

# This is the previous code, error: group matching query doesn't exist
# @allowed_users(allowed_roles=['Hall Provost'])
# def userlist(request):
#     users = User.objects.all()
#     userlist = []
#     for user in users:
#         userinfo = UserGroupForm()
#         userinfo.user = user
#         userinfo.group = Group.objects.get(user=user)
#         userlist.append(userinfo)
        
#     context = {'users':  userlist}
#     return render(request, 'accounts/index.html', context)

# Edited using chatgpt
@allowed_users(allowed_roles=['Hall Provost', ])
def userlist(request):
    userlist = []
    for user in User.objects.all():
        userinfo = UserGroupForm()
        userinfo.user = user
        userinfo.groups = ', '.join([str(i) for i in user.groups.values_list('name', flat=True)])  # Retrieve all groups associated with the user
        userlist.append(userinfo)
        
    context = {'users': userlist}
    return render(request, 'accounts/index.html', context)


@allowed_users(allowed_roles=['Hall Provost', ])
def edituser(request, userid):
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if request.method.is_valid():
        if request.POST.get("password1") != request.POST.get("password2"):
            messages.error(request, "Password and Confirm Password didn't match")
            return redirect('edituser', request.POST.get("id") )
            
        user = User.objects.get(id=request.POST.get("id"))
    
        if user.username != request.POST.get("username") and User.objects.filter(username = request.POST.get("username")).exists():
            messages.error(request, "username already exist")
            return redirect('edituser', request.POST.get("id") )
        
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        if request.POST.get("is_active") == "on":
            user.is_active = True
        else:
            user.is_active = False
        user.set_password(request.POST.get("password1"))
        user.save()
        user.groups.clear()
        user.groups.add(request.POST.get("group"))

        userinfo = UserProfile.objects.get(user=user)
        userinfo.fullName = user.first_name + " " + user.last_name
        userinfo.save()
        return redirect("userlist")
        
    userinfo = UserGroupForm()
    userinfo.user = User.objects.get(id=userid)
    userinfo.group = Group.objects.filter(user=userinfo.user)
    
    
    context = {'userinfo':  userinfo, 'groups': Group.objects.all()}
    return render(request, 'accounts/edit.html', context)


@allowed_users(allowed_roles=['Hall Provost'])
# def deleteuser(request):
#     if request.method == "POST":
#         user = User.objects.get(id=request.POST.get("userid"))
#         UserProfile.objects.get(user=user).delete()
#         user.delete()
        
#     return redirect('userlist')
def deleteuser(request):
    # Assuming you have some way of identifying the user whose profile you want to delete
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        # Delete the user profile
        user_profile.delete()
        # Optionally, delete the associated user as well
        # request.user.delete()
        # Redirect to a success page or somewhere else
        # return redirect('success_url')

    return redirect('userlist')
   

@allowed_users(allowed_roles=['Hall Provost', 'Student'])
def profile(request):
    if request.method == 'POST':
        userinfo = UserProfile.objects.get(user=request.user)
        userinfo.fullName = request.POST.get("fullName")
        userinfo.birthDate = request.POST.get("birthdate")
        userinfo.gender = request.POST.get("gender")
        userinfo.phone = request.POST.get("phone")
        userinfo.email = request.POST.get("email")
        userinfo.save()

        user = User.objects.get(pk=request.user.pk)
        user.email = request.POST.get("email")
        user.save()

        if userinfo.email == None:
            userinfo.email = user.email
            userinfo.save()

    if UserProfile.objects.filter(user=request.user).exists() == False:
        userinfo = UserProfile()
        userinfo.user = request.user
        userinfo.fullName = request.user.username
        userinfo.email = request.user.username + "@gmail.com"
        userinfo.entryDate = datetime.datetime.now()
        userinfo.save()

        user = User.objects.get(pk=request.user.pk)
        user.email = request.POST.get("email")
        user.save()

        if userinfo.email == None:
            userinfo.email = user.email
            userinfo.save()

    userinfo = UserProfile.objects.get(user=request.user)
    if userinfo.birthDate != None:
        birthdate = userinfo.birthDate.strftime('%Y-%m-%d')
    else:
        birthdate = datetime.datetime.now().strftime('%Y-%m-%d')
    userinfo.entryDate = userinfo.entryDate.strftime('%d-%m-%Y')

    

        
    addresses = Address.objects.filter(user=request.user)
    
    return render(request, 'core/profile.html',{
        'userinfo': userinfo,
        'birthdate':birthdate,
        'user': request.user,
        'addresses': addresses,
    })


@login_required(login_url='login')
def createaddressprofile(request):
    if request.method == 'POST':
        address = Address()
        address.user = request.user
        address.addressName = request.POST.get("addressName")
        address.country = request.POST.get("country")
        address.city = request.POST.get("city")
        address.area = request.POST.get("area")
        address.streetAddress = request.POST.get("streetaddress")
        address.save()
    else:
        return redirect("/profile/")
    return redirect("/profile/")


@login_required(login_url='login')
def deleteaddressprofile(request, id):
    if request.method == 'POST':
        Address.objects.filter(id=id).delete()
    else:
        return redirect("/profile/")
    return redirect("/profile/")


    if request.method == 'POST':
        order = Order.objects.get(ref_code=request.POST.get("ref_code"))
        order.status = 'CANCELLED'
        order.save()
        orderproducts = OrderProduct.objects.filter(order=order)
        for item in orderproducts:
            product = Product.objects.get(slug=item.item.slug)
            product.quantity += item.quantity
            product.sold -= item.quantity
            product.save()
    else:
        return redirect("/order/")
    return redirect("/order/")