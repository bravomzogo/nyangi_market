from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),  # Adjust this to the latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='use_whatsapp_for_recovery',
            field=models.BooleanField(default=True, help_text='Use WhatsApp as primary recovery method'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, help_text='WhatsApp number used for account recovery', max_length=15),
        ),
    ]
