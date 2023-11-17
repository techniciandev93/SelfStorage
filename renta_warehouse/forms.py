from django import forms
from django.contrib.auth.forms import UserChangeForm

from renta_warehouse.models import Order
from users.models import CustomUser


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        box = cleaned_data.get('box')
        if not box:
            return cleaned_data

        if box.orders.exists():
            raise forms.ValidationError('Этот бокс уже занят. Выберите другой бокс или убедитесь, что он свободен.')
        return cleaned_data


class CustomUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(label='Телефон', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Номер телефона',
    }))

    address = forms.CharField(label='Адрес', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Адрес доставки',
    }))

    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Ваше имя',
    }))

    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Ваша фамилия',
    }))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address')
