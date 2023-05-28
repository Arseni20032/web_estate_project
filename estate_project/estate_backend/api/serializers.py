import logging

from rest_framework import serializers
from ..models import Buyer, Owner, Employee, Estate, EstateType, Deal
import re

logger = logging.getLogger(__name__)


def validate_phone_number(value):
    pattern = r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError('Invalid phone number format. Expected format: +375 (29) XXX-XX-XX')


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

    def delete(self, instance):
        instance.delete()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        logger.info("Object %s was update" % instance)
        return instance


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = '__all__'

    def delete(self, instance):
        instance.delete()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        logger.info("Object %s was update" % instance)
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])
    buyers = BuyerSerializer(many=True)


    class Meta:
        model = Employee
        fields = '__all__'


class EstateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateType
        fields = '__all__'


class EstateSerializer(serializers.ModelSerializer):
    estate_type = EstateTypeSerializer()
    owner = OwnerSerializer()
    buyer = BuyerSerializer(many=True)
    responsible_employee = EmployeeSerializer()
    name = serializers.CharField(required=False)
    cost = serializers.FloatField(required=True)

    class Meta:
        model = Estate
        fields = '__all__'

    def delete(self, instance):
        instance.delete()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        logger.info("Object %s was update" % instance)
        return instance


class DealSerializer(serializers.ModelSerializer):
    estate = EstateSerializer()
    buyer = BuyerSerializer()
    employee = EmployeeSerializer()
    class Meta:
        model = Deal
        fields = '__all__'
