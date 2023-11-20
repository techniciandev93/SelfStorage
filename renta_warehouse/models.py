from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, IntegerField, Value, When, Case, CharField
from django.db.models.functions import TruncDate, Cast, Now
from django.utils.html import format_html

from users.models import CustomUser


class WareHouse(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    address = models.CharField(verbose_name='Адрес', max_length=200)
    temperature = models.FloatField(verbose_name='Температура')
    height = models.FloatField(verbose_name='Высота')
    advantage = models.CharField(verbose_name='Преимущество', max_length=150)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address

    def total_boxes(self):
        return self.boxes.count()

    def free_boxes(self):
        return self.boxes.filter(free=True).count()

    def get_preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>',
                               self.image.url)
        return 'Здесь будет изображение'

    get_preview_image.short_description = 'Вывод изображения'
    free_boxes.short_description = 'Свободно боксов'
    total_boxes.short_description = 'Всего боксов'


class BoxQuerySet(models.QuerySet):
    def rent_by_user(self, user_id):
        boxes_rent_by_user = Box.objects.filter(client__pk=user_id).values_list('box')
        return self.filter(pk__in=boxes_rent_by_user)


class Box(models.Model):
    number = models.IntegerField(verbose_name='Номер бокса')
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name='Склад', related_name='boxes')
    floor = models.IntegerField(verbose_name='Этаж')
    length = models.FloatField(verbose_name='Длина')
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    free = models.BooleanField(verbose_name='Свободный бокс', default=True)

    objects = BoxQuerySet.as_manager()

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'№ {self.number}. Склад {self.warehouse.address}'

    def square(self):
        if self.width and self.length:
            return self.width * self.length
        return 'Будет рассчитана площадь'

    square.short_description = 'Площадь бокса'


class OrderQuerySet(models.QuerySet):
    def user_orders(self, user_id):
        return self.filter(client__pk=user_id)

    def left_days(self):
        return self.annotate(
            left_days=Cast((TruncDate(F('end_rent_date')) - TruncDate(Now())), IntegerField()) / 86400000000) \
            .annotate(deadline=Case(
                When(left_days__lt=0, then=Value('expired')),
                When(left_days__gt=14, then=Value('far')),
                When(left_days__lte=14, then=Value('near')),
                output_field=CharField())
            )


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент', related_name='orders')
    box = models.ForeignKey(Box, on_delete=models.CASCADE, verbose_name='Бокс на складе', related_name='orders')
    start_rent_date = models.DateTimeField(verbose_name='Дата начала аренды', db_index=True)
    end_rent_date = models.DateTimeField(verbose_name='Плановая дата окончания аренды', db_index=True)
    warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка на склад')
    from_warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка со склада')
    actual_end_rent_date = models.DateTimeField(verbose_name='Фактическая дата окончания аренды',
                                                db_index=True, null=True, blank=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'ID заказа {self.id}'


class BoxImage(models.Model):
    box = models.ForeignKey(
        'Box',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Бокс')
    number = models.PositiveIntegerField(verbose_name='Порядковый номер изображения', default=0, db_index=True)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    class Meta:
        ordering = ['number']
        verbose_name = 'Изображение боксов'
        verbose_name_plural = 'Изображения боксов'

    def __str__(self):
        return f'Изображение № {self.number}, бокс № {self.box.number}'

    def get_preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>',
                               self.image.url)
        return 'Здесь будет изображение'

    get_preview_image.short_description = 'Вывод изображения'
