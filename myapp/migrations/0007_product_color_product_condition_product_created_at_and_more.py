# Generated by Django 5.1.5 on 2025-02-11 20:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_product_condition_remove_product_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='condition',
            field=models.CharField(default='New', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='dimensions',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='generation',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='release_year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AddField(
            model_name='product',
            name='warranty',
            field=models.CharField(default='No Warranty', max_length=50),
        ),
        migrations.AddField(
            model_name='seller',
            name='phone',
            field=models.CharField(default='N/A', max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.CharField(choices=[('Arusha', 'Arusha'), ('Dar es Salaam', 'Dar es Salaam'), ('Dodoma', 'Dodoma'), ('Geita', 'Geita'), ('Iringa', 'Iringa'), ('Kagera', 'Kagera'), ('Katavi', 'Katavi'), ('Kigoma', 'Kigoma'), ('Kilimanjaro', 'Kilimanjaro'), ('Lindi', 'Lindi'), ('Manyara', 'Manyara'), ('Mara', 'Mara'), ('Mbeya', 'Mbeya'), ('Morogoro', 'Morogoro'), ('Mtwara', 'Mtwara'), ('Mwanza', 'Mwanza'), ('Njombe', 'Njombe'), ('Pemba North', 'Pemba North'), ('Pemba South', 'Pemba South'), ('Rukwa', 'Rukwa'), ('Ruvuma', 'Ruvuma'), ('Shinyanga', 'Shinyanga'), ('Singida', 'Singida'), ('Simiyu', 'Simiyu'), ('Songwe', 'Songwe'), ('Tabora', 'Tabora'), ('Tanga', 'Tanga')], default='Dar es Salaam', max_length=50),
        ),
    ]
