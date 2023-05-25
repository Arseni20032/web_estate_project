from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OwnerSerializer, BuyerSerializer, DealSerializer, EmployeeSerializer, EstateSerializer, \
    EstateTypeSerializer, EstateAPIView, EmployeeAPIView, EstateViewSet, RatesView, JokeView
from rest_framework.authtoken.views import obtain_auth_token

app_name = "api"

router = DefaultRouter()
router.register(r'estate', EstateViewSet)

urlpatterns = [
# path('estate/', EstateAPIView.as_view(), name='estate_list'),
    path('token/', obtain_auth_token),
    path('employee/', EmployeeAPIView.as_view(), name='employee_list'),
    path('estate/list/', EstateAPIView.as_view(), name='estate_list'),
    path('', include(router.urls), name='estate_detail'),
    path('rates/', RatesView.as_view(), name='rates'),
    path('jokes/', JokeView.as_view(), name='jokes')



    # path(r'accounts', views.AccountAPIView.as_view(), name='account-list'),
    # path(r'contacts', views.ContactAPIView.as_view(), name='contact-list'),
    # path(r'activities', views.ActivityAPIView.as_view(), name='activity-list'),
    # path(r'activitystatuses', views.ActivityStatusAPIView.as_view(), name='activity-status-list'),
    # path(r'contactsources', views.ContactSourceAPIView.as_view(), name='contact-source-list'),
    # path(r'contactstatuses', views.ContactStatusAPIView.as_view(), name='contact-status-list')
]
