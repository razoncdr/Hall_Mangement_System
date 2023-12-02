from django.urls import path
from core import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('accounts/index/', views.userlist, name='userlist'),
    # path('accounts/logout/', views.logout, name='logout'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.registerpage, name='register'),
    path('accounts/login/', views.loginpage, name='login'),
    path('accounts/edit/<int:userid>', views.edituser, name='edituser'),
    path('accounts/delete/', views.deleteuser, name='deleteuser'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/createaddress/', views.createaddressprofile, name='createaddressprofile'),
    path('profile/deleteaddress/<int:id>', views.deleteaddressprofile, name='address_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)