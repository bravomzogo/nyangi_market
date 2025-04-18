# Generated by Django 5.1.5 on 2025-02-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_product_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.CharField(choices=[('Arusha', 'Arusha'), ('Dar es Salaam', 'Dar es Salaam'), ('Dodoma', 'Dodoma'), ('Geita', 'Geita'), ('Iringa', 'Iringa'), ('Kagera', 'Kagera'), ('Katavi', 'Katavi'), ('Kigoma', 'Kigoma'), ('Kilimanjaro', 'Kilimanjaro'), ('Lindi', 'Lindi'), ('Manyara', 'Manyara'), ('Mara', 'Mara'), ('Mbeya', 'Mbeya'), ('Morogoro', 'Morogoro'), ('Mtwara', 'Mtwara'), ('Mwanza', 'Mwanza'), ('Njombe', 'Njombe'), ('Pemba North', 'Pemba North'), ('Pemba South', 'Pemba South'), ('Rukwa', 'Rukwa'), ('Ruvuma', 'Ruvuma'), ('Shinyanga', 'Shinyanga'), ('Singida', 'Singida'), ('Simiyu', 'Simiyu'), ('Songwe', 'Songwe'), ('Tabora', 'Tabora'), ('Tanga', 'Tanga')], default='Dar es Salaam', max_length=50),
        ),
    ]
