# Generated by Django 5.0.2 on 2024-03-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0002_sliderproduct_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovari',
            name='sliders',
            field=models.ManyToManyField(default=None, related_name='slider_product', to='magazin.sliderproduct'),
        ),
    ]
