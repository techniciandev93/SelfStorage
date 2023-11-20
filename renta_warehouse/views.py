from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils import timezone

from renta_warehouse.forms import CustomUserForm, OrderDetailsForm
from users.models import CustomUser
from .models import Box, WareHouse, Order
from .service import create_payment_order


def index(request):
    return render(request, 'renta_warehouse/index.html')


@login_required(login_url='users:login')
def qr(request):
    return render(request, 'renta_warehouse/qr.html')


@login_required(login_url='users:login')
def get_my_rent(request):
    orders = Order.objects.user_orders(request.user.id).left_days()
    return render(
        request,
        template_name='renta_warehouse/my-rent.html',
        context={'orders': orders},
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
            'price_from': min([box.price for box in warehouse.boxes.all()], default=0),
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
        'id': box.pk,
        'flor': box.floor,
        'number': box.number,
        'square': box.square(),
        'price': box.price,
        'length': box.length,
        'width': box.width,
        'height': box.height,
        'size': (box.length, box.width, box.height),
    } for box in Box.objects.filter(free=True)]

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


@login_required(login_url='users:login')
def create_order(request):

    if request.method == 'POST':
        box_id = request.POST.get('box_details')
        user_email = request.POST.get('user')
        client = CustomUser.objects.get(email=user_email)
        box = Box.objects.get(pk=box_id)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30)

        new_order = Order.objects.create(
            client=client,
            box=box,
            start_rent_date=start_date,
            end_rent_date=end_date
        )

        payment_url = create_payment_order(amount=box.price, order_num=new_order.pk)
        context = {
            'order_id': new_order.pk,
            'client_email': new_order.client.email,
            'box_details': f'Склад: {box.warehouse.address}, '
                           f'номер бокса: {box.number}, '
                           f'этаж: {box.floor}, '
                           f'размеры бокса: { box.length } х { box.width } х { box.height } м², '
                           f'срок хранения с {start_date.strftime("%d/%m/%y")} по {end_date.strftime("%d/%m/%y")}',
            'payment_url': payment_url
        }
        return render(
            request,
            'renta_warehouse/order.html',
            context=context
        )

    else:
        return redirect('boxes')


def redirect_to_pay(request):
    if request.method == 'POST':
        user_contact = OrderDetailsForm(request.POST)
        if user_contact.is_valid():
            user_email = request.POST.get('user_email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            payment_url = request.POST.get('payment_url')
            user = CustomUser.objects.get(email=user_email)
            user.phone_number = phone_number
            user.address = address
            user.save()
            return redirect(payment_url)

        else:
            return redirect('boxes')
    else:
        return redirect('boxes')


def order_confirmation(request):
    order_number = request.GET.get('order')
    order = Order.objects.get(pk=order_number)
    order.paid = True
    box = order.box
    box.free = False
    order.save()
    box.save()
    return redirect('my_rent')
