# Generated by Django 5.1.5 on 2025-02-11 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='products/')),
                ('location', models.CharField(choices=[('Arusha', 'Arusha'), ('Dar es Salaam', 'Dar es Salaam'), ('Dodoma', 'Dodoma'), ('Geita', 'Geita'), ('Iringa', 'Iringa'), ('Kagera', 'Kagera'), ('Katavi', 'Katavi'), ('Kigoma', 'Kigoma'), ('Kilimanjaro', 'Kilimanjaro'), ('Lindi', 'Lindi'), ('Manyara', 'Manyara'), ('Mara', 'Mara'), ('Mbeya', 'Mbeya'), ('Morogoro', 'Morogoro'), ('Mtwara', 'Mtwara'), ('Mwanza', 'Mwanza'), ('Njombe', 'Njombe'), ('Pemba North', 'Pemba North'), ('Pemba South', 'Pemba South'), ('Rukwa', 'Rukwa'), ('Ruvuma', 'Ruvuma'), ('Shinyanga', 'Shinyanga'), ('Singida', 'Singida'), ('Simiyu', 'Simiyu'), ('Songwe', 'Songwe'), ('Tabora', 'Tabora'), ('Tanga', 'Tanga')], default='Arusha', max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='myapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('product_types', models.TextField(help_text='List of product categories sold, separated by commas')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.seller'),
        ),
    ]
