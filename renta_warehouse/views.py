from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from renta_warehouse.forms import CustomUserForm
from users.models import CustomUser
from .models import Box, WareHouse


def index(request):
    return render(
        request,
        'renta_warehouse/index.html',
    )


@login_required(login_url='index')
def get_my_rent(request):
    return render(
        request,
        'renta_warehouse/my-rent.html'
    )


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'renta_warehouse/my-rent.html'

    def get_success_url(self):
        return reverse_lazy('my_rent')


def get_boxes(request):
    warehouses = WareHouse.objects.all()
    warehouses_on_page = [
        {
            'full_address': warehouse.address,
            'city': warehouse.address.split(',')[0],
            'address': ', '.join(warehouse.address.split(',')[1:]).lstrip(),
            'boxes_free': warehouse.free_boxes(),
            'boxes_total': warehouse.total_boxes(),
            'price_from': 9999,
            'advantage': 'Тут должно быть преимущество',
            'number': warehouse.pk,
            'temperature': warehouse.temperature,
            'height': warehouse.height,
            'box_image_urls': [
                request.build_absolute_uri(image.image.url)
                for box in warehouse.boxes.all()
                for image in box.images.all()
            ]
        }
        for warehouse in warehouses
    ]

    return render(
        request,
        'renta_warehouse/boxes.html',
        context={
            'warehouses': warehouses_on_page
        }
    )



