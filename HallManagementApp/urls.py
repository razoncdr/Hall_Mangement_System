from django.urls import path
from HallManagementApp import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', RedirectView.as_view(url='/home/')),
    path('hall/create/', views.create_hall, name = 'create_hall'),
    path('hall/edit/<int:id>', views.edithall, name='edit_hall'),
    path('hall/delete/', views.deletehall, name = 'delete_hall'),
    path('hall/index/', views.hall_list, name='hall_list'),
    
    path('room/create/', views.create_room, name = 'create_room'),
    path('room/edit/<int:id>', views.editroom, name='edit_room'),
    path('room/delete/', views.deleteroom, name = 'delete_room'),
    path('room/index/', views.room_list, name='room_list'),
    
    path('batch/create/', views.create_batch, name = 'create_batch'),
    path('batch/edit/<int:id>', views.editbatch, name='edit_batch'),
    path('batch/delete/', views.deletebatch, name = 'delete_batch'),
    path('batch/index/', views.batch_list, name='batch_list'),
    
    path('department/create/', views.create_department, name = 'create_department'),
    path('department/edit/<int:id>', views.editdepartment, name='edit_department'),
    path('department/delete/', views.deletedepartment, name = 'delete_department'),
    path('department/index/', views.department_list, name='department_list'),
    
    path('session/create/', views.create_session, name = 'create_session'),
    path('session/edit/<int:id>', views.editsession, name='edit_session'),
    path('session/delete/', views.deletesession, name = 'delete_session'),
    path('session/index/', views.session_list, name='session_list'),
    
  
    path('student/create/', views.create_student, name = 'create_student'),
    path('student/edit/<int:id>', views.editstudent, name='edit_student'),
    path('student/delete/', views.deletestudent, name = 'delete_student'),
    path('student/index/', views.student_list, name='student_list'),
    
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)