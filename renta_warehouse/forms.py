from django import forms

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
