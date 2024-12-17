# Generated by Django 4.2.2 on 2024-11-27 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ECG_feat', '0005_key_ecg_models_key_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='customuser',
            name='key',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
