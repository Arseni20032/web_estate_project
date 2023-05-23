from rest_framework import generics
from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ..models import Owner, Buyer, Deal, Estate, EstateType, Employee
from .serializers import OwnerSerializer, BuyerSerializer, DealSerializer, EstateSerializer, EstateTypeSerializer, \
    EmployeeSerializer

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
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer


class EstateTypeAPIView(generics.ListCreateAPIView):
    queryset = EstateType.objects.all()
    serializer_class = EstateTypeSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]


class EstateApiDetailView(ModelViewSet):
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer
    lookup_field = 'id'

