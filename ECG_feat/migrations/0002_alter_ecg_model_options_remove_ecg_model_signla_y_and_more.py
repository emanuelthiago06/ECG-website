# Generated by Django 4.1.7 on 2023-06-05 11:27

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ECG_feat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ecg_model',
            options={'ordering': ['pk']},
        ),
        migrations.RemoveField(
            model_name='ecg_model',
            name='signla_y',
        ),
        migrations.RemoveField(
            model_name='ecg_model',
            name='user_name',
        ),
        migrations.AddField(
            model_name='ecg_model',
            name='signal_y',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ecg_model',
            name='signal_x',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
