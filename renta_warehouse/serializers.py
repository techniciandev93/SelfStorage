from rest_framework.serializers import ModelSerializer
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
