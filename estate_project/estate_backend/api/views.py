import logging

import requests
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .filters import EstateFilter
from .permissions import IsAdult
from .serializers import OwnerSerializer, BuyerSerializer, DealSerializer, EstateSerializer, EstateTypeSerializer, \
    EmployeeSerializer
from ..models import Owner, Buyer, Deal, Estate, EstateType, Employee

logger = logging.getLogger(__name__)
# Create your views here.


class OwnerAPIView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer




class BuyerAPIView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class DealAPIView(generics.ListCreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class EstateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAdult]
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer
    filterset_class = EstateFilter
    filter_backends = (filters.DjangoFilterBackend,)




class EstateTypeAPIView(generics.ListCreateAPIView):
    queryset = EstateType.objects.all()
    serializer_class = EstateTypeSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]


class EstateViewSet(ModelViewSet):
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

