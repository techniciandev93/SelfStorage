from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from renta_warehouse.forms import CustomUserForm
from users.models import CustomUser
from .models import Box, WareHouse, Order
from .serializers import BoxSerializer, OrderSerializer


def index(request):
    return render(
        request,
        'renta_warehouse/index.html',
    )


@login_required(login_url='index')
def get_my_rent(request):
    # rent_boxes = Box.objects.rent_by_user(request.user.id)
    orders = Order.objects.user_orders(request.user.id)
    serializer = OrderSerializer(orders, many=True)
    return render(
        request,
        template_name='renta_warehouse/my-rent.html',
        context={'orders': serializer.data}
    )


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'renta_warehouse/my-rent.html'

    def get_success_url(self):
        return reverse_lazy('my_rent')

    def get_queryset(self):
        queryset = CustomUser.objects.filter(id=self.request.user.id)
        return queryset


def get_boxes(request):
    warehouses = WareHouse.objects.all()
    warehouses_on_page = [
        {
            'full_address': warehouse.address,
            'warehouse_img': request.build_absolute_uri(warehouse.image.url),
            'city': warehouse.address.split(',')[0],
            'address': ', '.join(warehouse.address.split(',')[1:]).lstrip(),
            'boxes_free': warehouse.free_boxes(),
            'boxes_total': warehouse.total_boxes(),
            'price_from': min([box.price for box in warehouse.boxes.all()]),
            'advantage': warehouse.advantage,
            'number': warehouse.pk,
            'temperature': warehouse.temperature,
            'height': warehouse.height,
            'box_image_urls': [
                request.build_absolute_uri(image.image.url)
                for box in warehouse.boxes.all()
                for image in box.images.all()
            ],
        }
        for warehouse in warehouses
    ]

    boxes = [{
        'flor': box.floor,
        'number': box.number,
        'square': box.square(),
        'price': box.price,
        'length': box.length,
        'width': box.width,
        'height': box.height,
        'size': (box.length, box.width, box.height),
    } for box in Box.objects.all()]

    return render(
        request,
        'renta_warehouse/boxes.html',
        context={
            'warehouses': warehouses_on_page,
            'boxes': boxes
        }
    )


def get_faq(request):
    return render(
        request,
        'renta_warehouse/faq.html'
    )

