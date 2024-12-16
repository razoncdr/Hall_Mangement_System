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


def home(request):
    return render(request, 'home/index.html',{

    })


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


@allowed_users(allowed_roles=['Hall Provost', 'Admin'])
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

   
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm  # You can customize the form if needed

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)

        # Decode the uidb64 to get the user's ID
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)

        # Add the username to the context to display in the template
        context['username'] = user.username
        return context

    def form_valid(self, form):
        # Get the user from the token and uidb64
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        
        # Save user id in the session to use in the complete view
        self.request.session['reset_user'] = user.id
        
        # Continue with the parent form valid behavior
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        # Get the user from the session
        user_id = self.request.session.get('reset_user')
        if user_id:
            try:
                # Retrieve the user from the database
                user = User.objects.get(pk=user_id)
                # Send the reset email to the user
                self.send_reset_email(user)
                # Clear the session to prevent re-sending the email
                del self.request.session['reset_user']
            except User.DoesNotExist:
                pass
        
        return context

    def send_reset_email(self, user):
        subject = "Your Password Has Been Reset"
        message = f"Hello {user.username},\n\nYour password has been successfully reset. If you did not request this change, please contact support immediately."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list)



from django.shortcuts import render
from .forms import UserFilterForm
from django.contrib.auth.models import User

def userlist(request):
    form = UserFilterForm(request.GET or None)
    users = User.objects.none()  # Start with an empty queryset

    if request.method == "GET" and form.is_valid():
        username = form.cleaned_data.get('username', '')
        email = form.cleaned_data.get('email', '')
        is_active = form.cleaned_data.get('is_active', '')
        group = form.cleaned_data.get('group', None)

        # Debug information
        print("Form Data:")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Is Active: {is_active}")
        print(f"Group: {group}")


        users = User.objects.all()
        # Apply filters
        if username:
            users = users.filter(username__icontains=username)
        if email:
            users = users.filter(email__icontains=email)
        if is_active:
            is_active = is_active == '1'
            users = users.filter(is_active=is_active)
        if group:
            users = users.filter(groups=group)

        # Debug information
        print("Filtered Users:")
        print(users)

    return render(request, 'accounts/index.html', {'form': form, 'users': users})


@allowed_users(allowed_roles=['Hall Provost', 'Admin'])
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


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def deleteuser(request, userid):
    if request.method == 'POST':
        # Assuming you have some way of identifying the user whose profile you want to delete

        user = User.objects.get(id=userid)

        if Student.objects.filter(registration_number=user.username).exists():
            Student.objects.filter(registration_number=user.username).delete()

        if UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.filter(user=user).delete()

        # Optionally, delete the associated user as well
        user.delete()
        # Redirect to a success page or somewhere else
        # return redirect('success_url')

    return redirect('userlist')
   

@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'Student'])
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

      
    return render(request, 'core/profile.html',{
        'userinfo': userinfo,
        'birthdate':birthdate,
        'user': request.user,
    })


# @login_required(login_url='login')
# def createaddressprofile(request):
#     if request.method == 'POST':
#         address = Address()
#         address.user = request.user
#         address.addressName = request.POST.get("addressName")
#         address.country = request.POST.get("country")
#         address.city = request.POST.get("city")
#         address.area = request.POST.get("area")
#         address.streetAddress = request.POST.get("streetaddress")
#         address.save()
#     else:
#         return redirect("/profile/")
#     return redirect("/profile/")


# @login_required(login_url='login')
# def deleteaddressprofile(request, id):
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