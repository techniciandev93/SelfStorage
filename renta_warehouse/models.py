from django.core.validators import MinValueValidator
from django.db import models

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
        occupied_boxes = self.boxes.filter(orders__isnull=False).count()
        return self.total_boxes() - occupied_boxes

    free_boxes.short_description = 'Свободно боксов'
    total_boxes.short_description = 'Всего боксов'


class BoxQuerySet(models.QuerySet):
    def rent_by_user(self, user_id):
        boxes_rent_by_user = Order.objects.filter(client__pk=user_id).values_list('box')
        return self.filter(pk__in=boxes_rent_by_user)


class Box(models.Model):
    number = models.IntegerField(verbose_name='Номер бокса')
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE,  verbose_name='Склад', related_name='boxes')
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


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  verbose_name='Клиент', related_name='orders')
    box = models.ForeignKey(Box, on_delete=models.CASCADE,  verbose_name='Бокс на складе', related_name='orders')
    start_rent_date = models.DateTimeField(verbose_name='Дата начала аренды', db_index=True)
    end_rent_date = models.DateTimeField(verbose_name='Дата окончания аренды', db_index=True)
    warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка на склад')
    from_warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка со склада')
    actual_end_rent_date = models.DateTimeField(verbose_name='Фактическая дата окончания аренды',
                                                db_index=True, null=True, blank=True)

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
        verbose_name = 'Изображение боксов'
        verbose_name_plural = 'Изображения боксов'

    def __int__(self):
        return self.number
