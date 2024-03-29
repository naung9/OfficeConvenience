# Generated by Django 2.1.4 on 2019-03-01 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISGMStore', '0003_item_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchase_order',
            name='original_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.ImageField(default=None, upload_to='ISGMStore/images/'),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
