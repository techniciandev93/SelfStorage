from django.db import transaction
from django.shortcuts import get_object_or_404
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.fields import CharField, IntegerField, ChoiceField
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from .models import Box, Order


class BoxSerializer(ModelSerializer):
    class Meta:
        model = Box
        depth = 1
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        depth = 2
        fields = '__all__'
