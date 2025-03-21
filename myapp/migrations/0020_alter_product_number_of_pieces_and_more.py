# Generated by Django 5.1.5 on 2025-02-15 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_product_application_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='number_of_pieces',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='number_of_seats',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='pages',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weather_resistant',
            field=models.BooleanField(blank=True, default='', null=True),
        ),
    ]
