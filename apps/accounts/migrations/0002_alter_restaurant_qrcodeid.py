# Generated by Django 5.1.6 on 2025-03-16 18:13

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='qrCodeID',
            field=models.CharField(default=apps.accounts.models.generate_unique_qr_code, max_length=16, unique=True),
        ),
    ]
