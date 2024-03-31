# Generated by Django 5.0.2 on 2024-03-17 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('avatar', models.ImageField(default='avatars/default.png', upload_to='avatars/')),
                ('phone', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('balance', models.IntegerField(default=0, verbose_name='Баланс')),
            ],
        ),
        migrations.CreateModel(
            name='SliderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliders/', verbose_name='Фото товара')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tovari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название товара')),
                ('description', models.TextField(verbose_name='Описание товара')),
                ('image', models.ImageField(upload_to='tovari/', verbose_name='Фото товара')),
                ('price', models.IntegerField(verbose_name='Цена товара')),
                ('count', models.IntegerField(verbose_name='Количество товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.category', verbose_name='Категория')),
                ('sliders', models.ManyToManyField(default=False, related_name='slider_product', to='magazin.sliderproduct')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazin.client')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus', to='magazin.status')),
                ('products', models.ManyToManyField(related_name='order_products', to='magazin.tovari')),
            ],
        ),
    ]