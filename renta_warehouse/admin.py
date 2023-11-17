from django.contrib import admin

from renta_warehouse.forms import OrderAdminForm
from renta_warehouse.models import Client, WareHouse, Box, Order, BoxImage


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    fields = ('number', 'warehouse', 'floor', 'length', 'width', 'height', 'square')
    readonly_fields = ('square',)


@admin.register(WareHouse)
class WareHouseAdmin(admin.ModelAdmin):
    fields = ('address', 'temperature', 'height', 'free_boxes', 'total_boxes')
    readonly_fields = ('free_boxes', 'total_boxes')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(BoxImage)
class BoxImageAdmin(admin.ModelAdmin):
    list_display = ['number']
    raw_id_fields = ['box']