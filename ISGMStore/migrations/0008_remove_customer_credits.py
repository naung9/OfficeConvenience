# Generated by Django 2.2.1 on 2019-08-06 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ISGMStore', '0007_order_history_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='credits',
        ),
    ]