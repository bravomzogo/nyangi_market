# Generated by Django 5.1.5 on 2025-02-09 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_product_technical_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='technical_details',
        ),
    ]
