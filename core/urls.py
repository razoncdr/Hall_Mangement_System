import django
from django.urls import path
from core import views, setupviews, reportviews
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.home, name='home'),
    # path('home/<slug:id>', views.DynamicPage, name='DynamicPage'),
    # path('about/', views.about, name='about'),
    
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.registerpage, name='register'),
    path('accounts/login/', views.loginpage, name='login'),
    path('accounts/edit/<int:userid>', views.edituser, name='edituser'),
    path('accounts/delete/', views.deleteuser, name='deleteuser'),
    path('accounts/index/', views.userlist, name='userlist'),
    
    path('feeshead/create/', setupviews.createfeeshead, name = 'create_feeshead'),
    path('feeshead/edit/<int:id>', setupviews.editfeeshead, name='edit_feeshead'),
    path('feeshead/delete/', setupviews.deletefeeshead, name = 'delete_feeshead'),
    path('feeshead/index/', setupviews.feesheadlist, name='feeshead_list'),

    path('studentfee/index/', setupviews.studentfeelist, name='studentfeelist'),
    path('studentfee/generate/', setupviews.generatestudentfee, name='generate_studentfee'),
    path('studentfee/create/', setupviews.createstudentfee, name='create_studentfee'),
    path('studentfee/delete/', setupviews.deletestudentfee, name='delete_studentfee'),

    path('report/fee_statement/', reportviews.feestatementreport, name='fee_statement_report'),
    path('report/fee_payment/', reportviews.feestatementreport, name='fee_payment_report'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/createaddress/', views.createaddressprofile, name='createaddressprofile'),
    path('profile/deleteaddress/<int:id>', views.deleteaddressprofile, name='address_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)