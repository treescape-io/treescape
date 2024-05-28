# Generated by Django 5.0.4 on 2024-05-26 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forest_designs', '0007_kind_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantimage',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='plantlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Timestamp of the log entry.', verbose_name='date'),
        ),
    ]