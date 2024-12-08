# Generated by Django 5.0.4 on 2024-12-09 15:10

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forest_designs', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantState',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'plant state',
                'verbose_name_plural': 'plant states',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='plant',
            name='notes',
        ),
        migrations.AlterField(
            model_name='plantlog',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now, help_text='Timestamp of the log entry.', verbose_name='date'),
        ),
        migrations.CreateModel(
            name='PlantStateTransition',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now, help_text='Moment of state transition.', verbose_name='date')),
                ('plant', models.ForeignKey(db_column='plant_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='statetransitions', to='forest_designs.plant')),
                ('state', models.ForeignKey(db_column='state_uuid', help_text='State to transition to.', on_delete=django.db.models.deletion.PROTECT, related_name='transitions', to='forest_designs.plantstate')),
            ],
            options={
                'verbose_name': 'plant state transition',
                'verbose_name_plural': 'plant state transitions',
                'ordering': ['-date'],
            },
        ),
    ]
