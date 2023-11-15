from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from users.froms import CustomAuthenticationForm


def index(request):
    form = CustomAuthenticationForm()
    return render(request, 'renta_warehouse/index.html', context={'form': form})
