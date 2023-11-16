from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from renta_warehouse.forms import CustomUserForm
from users.models import CustomUser


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
    return render(
        request,
        'renta_warehouse/boxes.html'
    )
