# Generated by Django 5.1.5 on 2025-02-15 18:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_product_application_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='application_method',
        ),
        migrations.RemoveField(
            model_name='product',
            name='assembly_required',
        ),
        migrations.RemoveField(
            model_name='product',
            name='author',
        ),
        migrations.RemoveField(
            model_name='product',
            name='battery_life',
        ),
        migrations.RemoveField(
            model_name='product',
            name='battery_required',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='product',
            name='certification',
        ),
        migrations.RemoveField(
            model_name='product',
            name='charging_time',
        ),
        migrations.RemoveField(
            model_name='product',
            name='closure_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='connectivity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='dietary_info',
        ),
        migrations.RemoveField(
            model_name='product',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='product',
            name='engine_capacity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='fabric_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='fuel_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gemstone',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='product',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='product',
            name='interactive_features',
        ),
        migrations.RemoveField(
            model_name='product',
            name='language',
        ),
        migrations.RemoveField(
            model_name='product',
            name='material_durability',
        ),
        migrations.RemoveField(
            model_name='product',
            name='metal_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='mileage',
        ),
        migrations.RemoveField(
            model_name='product',
            name='number_of_pieces',
        ),
        migrations.RemoveField(
            model_name='product',
            name='number_of_seats',
        ),
        migrations.RemoveField(
            model_name='product',
            name='origin_country',
        ),
        migrations.RemoveField(
            model_name='product',
            name='package_size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='product',
            name='paper_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='power_consumption',
        ),
        migrations.RemoveField(
            model_name='product',
            name='processor',
        ),
        migrations.RemoveField(
            model_name='product',
            name='publisher',
        ),
        migrations.RemoveField(
            model_name='product',
            name='recommended_age',
        ),
        migrations.RemoveField(
            model_name='product',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='product',
            name='safety_certifications',
        ),
        migrations.RemoveField(
            model_name='product',
            name='scent',
        ),
        migrations.RemoveField(
            model_name='product',
            name='screen_size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='shoe_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='skin_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sport_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='storage_capacity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='style',
        ),
        migrations.RemoveField(
            model_name='product',
            name='top_speed',
        ),
        migrations.RemoveField(
            model_name='product',
            name='transmission',
        ),
        migrations.RemoveField(
            model_name='product',
            name='upholstery_material',
        ),
        migrations.RemoveField(
            model_name='product',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='product',
            name='washing_instructions',
        ),
        migrations.RemoveField(
            model_name='product',
            name='water_resistant',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weather_resistant',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight_capacity',
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(default='New', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='dimensions',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='generation',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='release_year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.CharField(default='No Warranty', max_length=50),
        ),
    ]
