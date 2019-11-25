# Generated by Django 2.1.4 on 2019-03-01 07:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISGMStore', '0004_auto_20190301_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='discount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='discount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(80)]),
        ),
    ]