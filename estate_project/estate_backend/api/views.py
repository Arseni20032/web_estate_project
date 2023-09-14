import logging
from io import BytesIO

import requests
from django.db.models import Sum, Count
from django.http import HttpResponse
from django_filters import rest_framework as filters
from matplotlib import pyplot as plt
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import EstateFilter
from .permissions import IsAdult, IsEmployee
from .serializers import OwnerSerializer, BuyerSerializer, DealSerializer, EstateSerializer, EstateTypeSerializer, \
    EmployeeSerializer
from ..models import Owner, Buyer, Deal, Estate, EstateType, Employee

logger = logging.getLogger(__name__)
# Create your views here.


class OwnerViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, IsAdult]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class BuyerViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, IsAdult]
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, IsAdult]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DealViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, IsAdult]
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class BuyerAPIView(generics.ListCreateAPIView):
    """для отображения связи текущего сотрудника с его покупателями"""
    permission_classes = [IsAuthenticated, IsEmployee]
    serializer_class = BuyerSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            return Buyer.objects.filter(deal__employee=employee)
        except Employee.DoesNotExist:
            return Buyer.objects.none()


class ProfitableEstateTypeView(APIView):
    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):
        # Получаем тип недвижимости с наибольшей прибылью
        estate_types = EstateType.objects.all()
        estate_type_profit = {}

        for estate_type in estate_types:
            total_profit = estate_type.estate_set.aggregate(total_profit=Sum('cost'))['total_profit']

            if total_profit:
                estate_type_profit[estate_type.type_estate] = total_profit

        if estate_type_profit:
            # Получаем тип недвижимости с наибольшей прибылью
            max_profit_estate_type = max(estate_type_profit, key=estate_type_profit.get)

            # Возвращаем результаты
            return Response({
                'estate_type': max_profit_estate_type,
                'total_profit': estate_type_profit[max_profit_estate_type]
            })
        else:
            # Если нет типов недвижимости, возвращаем пустой ответ
            return Response({
                'estate_type': None,
                'total_profit': 0
            })


class EstateAPIView(generics.ListCreateAPIView):
    """Публичное представление недвижимости для незарегистрированных пользователей"""
    permission_classes = [AllowAny]
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer
    filterset_class = EstateFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = [SearchFilter, OrderingFilter, filters.DjangoFilterBackend]
    search_fields = ['name', 'description', 'address']  # Поля, по которым будет выполняться поиск
    ordering_fields = ['name', 'creation_date', 'cost']  # Поля, по которым будет выполняться сортировка


class EstateStatsView(APIView):
    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):
        # Получаем сумму стоимости и количество сделок
        total_cost = Deal.objects.aggregate(total_cost=Sum('cost'))['total_cost']
        total_deals = Deal.objects.count()

        # Возвращаем результаты
        return Response({
            'total_cost': total_cost,
            'total_deals': total_deals
        })


class EstateTypeAPIView(generics.ListCreateAPIView):
    queryset = EstateType.objects.all()
    serializer_class = EstateTypeSerializer


class EstateViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, IsAdult]
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer


class RatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            'content': self.fetch_rates(),
            'status': 'success'
        }
        return Response(data)

    def fetch_rates(self):
        response = requests.get("https://api.nbrb.by/exrates/rates?periodicity=0")
        logger.info('Request to API NBRB: %s' % response.status_code)
        response_data = response.json()
        rates_list = ['USD', 'EUR', 'RUB']
        return {rate['Cur_Abbreviation']: rate['Cur_OfficialRate'] for rate in response_data if
        rate['Cur_Abbreviation'] in rates_list}


class JokeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            'content': self.fetch_joke(),
            'status': 'success'
        }
        return Response(data)

    def fetch_joke(self):
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        logger.info('Request to joke API: %s' % response.status_code)
        response_data = response.json()
        return response_data


class UserTimezoneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        timezone = request.user.timezone
        return Response({'timezone': timezone})


class DealStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Используем агрегацию для получения статистики по количеству Deal по deal_date
        deal_stats = Deal.objects.values('deal_date').annotate(deal_count=Count('id')).order_by('deal_date')

        # Разделяем данные статистики на метки (labels) и значения (counts)
        labels = [stat['deal_date'].strftime('%Y-%m-%d') for stat in deal_stats]
        counts = [stat['deal_count'] for stat in deal_stats]

        # Создаем график
        plt.figure(figsize=(11, 7))
        plt.plot(labels, counts)
        plt.xlabel('Date')
        plt.ylabel('Deal Count')
        plt.title('Deal Statistics')
        plt.grid(True)

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Возвращаем ответ с данными изображения
        image_stream.seek(0)
        response = HttpResponse(content_type='image/png')
        response.write(image_stream.getvalue())
        return response

