from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic.base import RedirectView

from core import views, setupviews, reportviews, studentviews, paymentviews
from core.api.views import CreateSSLCommerzCheckoutSessionView, \
    SSLCommerzPaymentCaptureView
from core.views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.home, name='home'),

    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.registerpage, name='register'),
    path('accounts/login/', views.loginpage, name='login'),
    path('accounts/edit/<int:userid>', views.edituser, name='edituser'),
    path('accounts/delete/<int:userid>', views.deleteuser, name='deleteuser'),
    path('accounts/index/', views.userlist, name='userlist'),

    # Request password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
      template_name='password_reset/password_reset_form.html'
    ), name='password_reset'),

    # Password reset email sent confirmation
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
      template_name='password_reset/password_reset_done.html'
    ), name='password_reset_done'),

    # Password reset link confirmation
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='password_reset/password_reset_confirm.html'
    # ), name='password_reset_confirm'),

    # Password Reset Confirmation URL
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(
      template_name='password_reset/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Password Reset Complete
    path('reset/done/', CustomPasswordResetCompleteView.as_view(
      template_name='password_reset/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('profile/', views.profile, name='profile'),

    path('hall/create/', setupviews.create_hall, name='create_hall'),
    path('hall/edit/<int:id>', setupviews.edithall, name='edit_hall'),
    path('hall/delete/', setupviews.deletehall, name='delete_hall'),
    path('hall/index/', setupviews.hall_list, name='hall_list'),

    path('room/create/', setupviews.create_room, name='create_room'),
    path('room/edit/<int:id>', setupviews.editroom, name='edit_room'),
    path('room/delete/', setupviews.deleteroom, name='delete_room'),
    path('room/index/', setupviews.room_list, name='room_list'),

    path('batch/create/', setupviews.create_batch, name='create_batch'),
    path('batch/edit/<int:id>', setupviews.editbatch, name='edit_batch'),
    path('batch/delete/', setupviews.deletebatch, name='delete_batch'),
    path('batch/index/', setupviews.batch_list, name='batch_list'),

    path('department/create/', setupviews.create_department, name='create_department'),
    path('department/edit/<int:id>', setupviews.editdepartment, name='edit_department'),
    path('department/delete/', setupviews.deletedepartment, name='delete_department'),
    path('department/index/', setupviews.department_list, name='department_list'),

    path('session/create/', setupviews.create_session, name='create_session'),
    path('session/edit/<int:id>', setupviews.editsession, name='edit_session'),
    path('session/delete/', setupviews.deletesession, name='delete_session'),
    path('session/index/', setupviews.session_list, name='session_list'),

    path('semester/create/', setupviews.create_semester, name='create_semester'),
    path('semester/edit/<int:id>', setupviews.edit_semester, name='edit_semester'),
    path('semester/delete/', setupviews.delete_semester, name='delete_semester'),
    path('semester/index/', setupviews.semester_list, name='semester_list'),

    path('applications/create/', studentviews.dormitoryApplicationCreate, name='application_create'),
    path('verify-email/<uuid:uuid>/<str:token>/', studentviews.verify_email, name='verify_email'),
    path('applications/review/<int:id>', studentviews.review_dormitoryApplication,
       name='application_review'),
    path('applications/<uuid:uuid>/<str:token>/update/', studentviews.update_dormitoryApplication,
       name='application_update'),
    path('applications/delete/', studentviews.delete_dormitoryApplication, name='application_delete'),
    path('applications/index/', studentviews.dormitoryApplication_list, name='application_list'),

    path('student/create/', setupviews.create_student, name='create_student'),
    path('student/edit/<int:id>', setupviews.editstudent, name='edit_student'),
    path('student/delete/', setupviews.deletestudent, name='delete_student'),
    path('student/index/', setupviews.student_list, name='student_list'),

    path('feeshead/create/', setupviews.createfeeshead, name='create_feeshead'),
    path('feeshead/edit/<int:id>', setupviews.editfeeshead, name='edit_feeshead'),
    path('feeshead/delete/', setupviews.deletefeeshead, name='delete_feeshead'),
    path('feeshead/index/', setupviews.feesheadlist, name='feeshead_list'),

    path('student-fee/index/', setupviews.studentfeelist, name='studentfeelist'),
    path('student-fee/generate/', setupviews.generatestudentfee, name='generate_studentfee'),
    path('student-fee/create/', setupviews.createstudentfee, name='create_studentfee'),
    path('student-fee/delete/', setupviews.deletestudentfee, name='delete_studentfee'),

    path('student-fee/payment/', paymentviews.fee_payment, name='student_fee_payment'),
    path('student-fee/payment-history/', paymentviews.fee_payment_history, name='fee_payment_history'),
    path('student-fee/payment-success/', paymentviews.payment_success, name='payment_success'),
    path('student-fee/payment-cancel/', paymentviews.payment_cancel, name='payment_cancel'),
    path('student-fee/payment-fail/', paymentviews.payment_fail, name='payment_fail'),

    path('report/fee-transaction/', reportviews.fee_transaction_report, name='fee_transaction_report'),
    path('report/fee-payment/', reportviews.fee_transaction_report, name='fee_payment_report'),

    path(
        'api/payment/sslcommerz/checkout/',
        CreateSSLCommerzCheckoutSessionView.as_view(),
        name='sslcommerz_checkout'
    ),

    path(
      'api/payment/sslcommerz/capture/',
      SSLCommerzPaymentCaptureView.as_view(),
      name='sslcommerz_capture'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)