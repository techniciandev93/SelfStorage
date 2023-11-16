from django import forms
from django.contrib.auth.forms import UserCreationForm

from renta_warehouse.models import Order
from users.models import CustomUser


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        box = cleaned_data.get('box')
        if box.orders.exists():
            raise forms.ValidationError('Этот бокс уже занят. Выберите другой бокс или убедитесь, что он свободен.')
        return cleaned_data


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'autofocus': True,
        'class': 'form-control fs_24 ps-2 SelfStorage__input',
        'placeholder': 'Email'
    }))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

