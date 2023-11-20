from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from renta_warehouse.forms import OrderAdminForm
from renta_warehouse.models import WareHouse, Box, Order, BoxImage


class IsExpiredFilter(admin.SimpleListFilter):
    title = 'Просроченные заказы'
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Просрочены'),
            ('No', 'Не просрочены'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.left_days().filter(deadline='expired')
        elif value == 'No':
            return queryset.left_days().exclude(deadline='expired')
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'phone_number',
        'address',
        'box',
        'start_rent_date',
        'end_rent_date',
    ]
    list_filter = [
        IsExpiredFilter,
        'warehouse_delivery',
        'from_warehouse_delivery',
    ]

    @admin.display(description='Телефон')
    def phone_number(self, obj):
        return obj.client.phone_number

    @admin.display(description='Адрес')
    def address(self, obj):
        return obj.client.address

    form = OrderAdminForm

    def save_model(self, request, obj, form, change):
        if obj.actual_end_rent_date:
            obj.box.free = False
            obj.box.save()
        else:
            obj.box.free = True
            obj.box.save()
        super().save_model(request, obj, form, change)


class BoxImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = BoxImage
    fields = ('image', 'get_preview_image')
    readonly_fields = ('get_preview_image',)
    extra = 0


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    fields = ('number', 'warehouse', 'floor', 'length', 'width', 'height', 'square', 'price', 'free')
    readonly_fields = ('square', 'free')
    raw_id_fields = ['warehouse']

    inlines = [
        BoxImageInline,
    ]


@admin.register(WareHouse)
class WareHouseAdmin(admin.ModelAdmin):
    fields = ('address', 'temperature', 'height', 'free_boxes', 'total_boxes', 'image', 'get_preview_image', 'advantage')
    readonly_fields = ('free_boxes', 'total_boxes', 'get_preview_image')


@admin.register(BoxImage)
class BoxImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    raw_id_fields = ('box',)

    fields = ('box', 'image', 'get_preview_image')
    readonly_fields = ('get_preview_image',)
