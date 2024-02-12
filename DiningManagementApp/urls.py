from django.urls import path
from DiningManagementApp import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from .views import add_dining_manager, add_member

urlpatterns = [
    # path('', RedirectView.as_view(url='/home/')),
    
    path('dining/members/', views.member_list, name='member_list'),
    path('dining/dining_managers/', views.dining_manager_list, name='dining_manager_list'),
    path('add_dining_manager/', add_dining_manager, name='add_dining_manager'),
    path('add_member/', add_member, name='add_member'),
    
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
