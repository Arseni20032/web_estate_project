from django.urls import path, include
from .views import OwnerSerializer, BuyerSerializer, DealSerializer, EmployeeSerializer, EstateSerializer, \
    EstateTypeSerializer, EstateAPIView, EmployeeAPIView, EstateApiDetailView
from rest_framework.authtoken.views import obtain_auth_token

app_name = "api"

urlpatterns = [
    path('estate/', EstateAPIView.as_view(), name='estate_list'),
    path('token/', obtain_auth_token),
    path('employee/', EmployeeAPIView.as_view(), name='employee_list'),
    path('estate/<int:id>/', EstateApiDetailView.as_view({'delete': 'destroy'}), name='estate-detail'),
    # path(r'accounts', views.AccountAPIView.as_view(), name='account-list'),
    # path(r'contacts', views.ContactAPIView.as_view(), name='contact-list'),
    # path(r'activities', views.ActivityAPIView.as_view(), name='activity-list'),
    # path(r'activitystatuses', views.ActivityStatusAPIView.as_view(), name='activity-status-list'),
    # path(r'contactsources', views.ContactSourceAPIView.as_view(), name='contact-source-list'),
    # path(r'contactstatuses', views.ContactStatusAPIView.as_view(), name='contact-status-list')
]
