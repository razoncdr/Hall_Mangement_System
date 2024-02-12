from django.urls import path
from HallManagementApp import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', RedirectView.as_view(url='/home/')),
    path('student/create/', views.create_student, name = 'create_student'),
    path('student/edit/<int:id>', views.editstudent, name='edit_student'),
    path('student/delete/', views.deletestudent, name = 'delete_student'),
    path('student/index/', views.student_list, name='student_list'),
    
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)