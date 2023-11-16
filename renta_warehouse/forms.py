from django import forms
from .models import CustomUser
from renta_warehouse.models import Order


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


class ContactForm(forms.Form):
    EMAIL1 = forms.EmailField()


class LoginForm(forms.Form):
    EMAIL = forms.EmailField()
    PASSWORD = forms.CharField()


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    PASSWORD_CREATE = forms.CharField()
    PASSWORD_CONFIRM = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['PASSWORD_CREATE'] != cd['PASSWORD_CONFIRM']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['PASSWORD_CONFIRM']
