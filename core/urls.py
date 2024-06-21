import django
from django.urls import path
from core import views, setupviews, reportviews, studentviews
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
    
    path('profile/', views.profile, name='profile'),

    path('hall/create/', setupviews.create_hall, name = 'create_hall'),
    path('hall/edit/<int:id>', setupviews.edithall, name='edit_hall'),
    path('hall/delete/', setupviews.deletehall, name = 'delete_hall'),
    path('hall/index/', setupviews.hall_list, name='hall_list'),
    
    path('room/create/', setupviews.create_room, name = 'create_room'),
    path('room/edit/<int:id>', setupviews.editroom, name='edit_room'),
    path('room/delete/', setupviews.deleteroom, name = 'delete_room'),
    path('room/index/', setupviews.room_list, name='room_list'),
    
    path('batch/create/', setupviews.create_batch, name = 'create_batch'),
    path('batch/edit/<int:id>', setupviews.editbatch, name='edit_batch'),
    path('batch/delete/', setupviews.deletebatch, name = 'delete_batch'),
    path('batch/index/', setupviews.batch_list, name='batch_list'),
    
    path('department/create/', setupviews.create_department, name = 'create_department'),
    path('department/edit/<int:id>', setupviews.editdepartment, name='edit_department'),
    path('department/delete/', setupviews.deletedepartment, name = 'delete_department'),
    path('department/index/', setupviews.department_list, name='department_list'),
    
    path('session/create/', setupviews.create_session, name = 'create_session'),
    path('session/edit/<int:id>', setupviews.editsession, name='edit_session'),
    path('session/delete/', setupviews.deletesession, name = 'delete_session'),
    path('session/index/', setupviews.session_list, name='session_list'),
  
    path('semester/create/', setupviews.create_semester, name = 'create_semester'),
    path('semester/edit/<int:id>', setupviews.edit_semester, name='edit_semester'),
    path('semester/delete/', setupviews.delete_semester, name = 'delete_semester'),
    path('semester/index/', setupviews.semester_list, name='semester_list'),

    path('applications/create/', studentviews.dormitoryApplicationCreate, name='application_create'),
    path('student/create/', setupviews.create_student, name = 'create_student'),
    path('student/edit/<int:id>', setupviews.editstudent, name='edit_student'),
    path('student/delete/', setupviews.deletestudent, name = 'delete_student'),
    path('student/index/', setupviews.student_list, name='student_list'),


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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)