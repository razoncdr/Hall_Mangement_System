from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('communication/provost_notice/', views.provost_notice, name='provost_notice'),
    path('communication/submit_notice/', views.submit_notice, name='submit_notice'),
    path('communication/provost-notices/', views.provost_notices, name='provost_notices'),
    path('delete-notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),


]
