# Generated by Django 5.1.7 on 2025-07-20 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_order_product_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.payment'),
        ),
    ]
