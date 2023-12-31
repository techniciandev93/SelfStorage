# Generated by Django 3.2.23 on 2023-11-20 06:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер бокса')),
                ('floor', models.IntegerField(verbose_name='Этаж')),
                ('length', models.FloatField(verbose_name='Длина')),
                ('width', models.FloatField(verbose_name='Ширина')),
                ('height', models.FloatField(verbose_name='Высота')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)], verbose_name='цена')),
                ('free', models.BooleanField(default=True, verbose_name='Свободный бокс')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
        migrations.CreateModel(
            name='BoxImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Порядковый номер изображения')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение боксов',
                'verbose_name_plural': 'Изображения боксов',
            },
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('temperature', models.FloatField(verbose_name='Температура')),
                ('height', models.FloatField(verbose_name='Высота')),
                ('advantage', models.CharField(max_length=150, verbose_name='Преимущество')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_rent_date', models.DateTimeField(db_index=True, verbose_name='Дата начала аренды')),
                ('end_rent_date', models.DateTimeField(db_index=True, verbose_name='Плановая дата окончания аренды')),
                ('warehouse_delivery', models.BooleanField(default=False, verbose_name='Доставка на склад')),
                ('from_warehouse_delivery', models.BooleanField(default=False, verbose_name='Доставка со склада')),
                ('actual_end_rent_date', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Фактическая дата окончания аренды')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='renta_warehouse.box', verbose_name='Бокс на складе')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
