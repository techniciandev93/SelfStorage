from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login

from .models import CustomUser


def index(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        login_form = LoginForm(request.POST)
        user_form = UserRegistrationForm(request.POST)
        if contact_form.is_valid():
            cd = contact_form.cleaned_data
            subject = "Рассчет стоимости"
            message = f'{cd["EMAIL1"]} запросил рассчет стоимости'
            send_mail(subject, message,
                      'selfstorage395@gmail.com',
                      ['selfstorage395@gmail.com'])
        elif login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                            request,
                            username=cd['EMAIL'],
                            password=cd['PASSWORD']
                        )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('my_rent')
            else:
                return HttpResponse('Invalid login')
        elif user_form.is_valid():
            new_user = user_form.save(commit=False)
            print(new_user)
            new_user.set_password(user_form.cleaned_data['PASSWORD_CONFIRM'])
            new_user.save()
            print(new_user)
            return redirect('my_rent')
        else:
            print(user_form.errors)

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


def get_boxes(request):
    return render(
        request,
        'renta_warehouse/boxes.html'
    )


