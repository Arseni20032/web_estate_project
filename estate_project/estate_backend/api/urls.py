from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import EstateAPIView, EstateViewSet, RatesView, JokeView, BuyerAPIView, \
    OwnerViewSet, BuyerViewSet, EmployeeViewSet, DealViewSet, UserTimezoneView, EstateTypeAPIView, EstateStatsView, \
    ProfitableEstateTypeView, DealStatsAPIView

app_name = "api"

"""маршрутизатор для CRUD"""
router = DefaultRouter()
router.register(r'estate', EstateViewSet)
router.register(r'owner', OwnerViewSet)
router.register(r'buyer', BuyerViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'deal', DealViewSet)

urlpatterns = [
    path('deal-stats-graph/', DealStatsAPIView.as_view(), name='deal_stats_graph'),
    path('estate/stats/', EstateStatsView.as_view(), name='estate_stats'),
    path('estate/profitable-type/', ProfitableEstateTypeView.as_view(), name='profitable_estate_type'),
    path('token/', obtain_auth_token),
    path('estate/list/', EstateAPIView.as_view(), name='estate_list'),
    path('rates/', RatesView.as_view(), name='rates'),
    path('jokes/', JokeView.as_view(), name='jokes'),
    path('employee_buyers/', BuyerAPIView.as_view(), name='buyers'),
    path('estate_type/', EstateTypeAPIView.as_view(), name='estate_type'),
    path('user/timezone/', UserTimezoneView.as_view(), name='user_timezone'),
    path('', include(router.urls)),
]
