# Generated by Django 5.0.4 on 2024-12-20 17:22

import datetime
import django.contrib.gis.db.models.fields
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant_species', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantImageKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'plant image type',
                'verbose_name_plural': 'plant image types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlantLogKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'plant log type',
                'verbose_name_plural': 'plant log types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlantState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
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
        migrations.CreateModel(
            name='ZoneKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'zone type',
                'verbose_name_plural': 'zone types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, unique=True, verbose_name='location')),
                ('genus', models.ForeignKey(blank=True, db_column='genus_uuid', on_delete=django.db.models.deletion.PROTECT, to='plant_species.genus', to_field='uuid')),
                ('species', models.ForeignKey(blank=True, db_column='species_uuid', help_text='When specified, genus is automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.species', to_field='uuid')),
                ('variety', models.ForeignKey(blank=True, db_column='variety_uuid', help_text='When specified, species and genus are automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.speciesvariety', to_field='uuid')),
            ],
            options={
                'verbose_name': 'plant',
                'verbose_name_plural': 'plants',
            },
        ),
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime.now, verbose_name='date')),
                ('image', models.ImageField(upload_to='plant_images', verbose_name='image')),
                ('plant', models.ForeignKey(db_column='plant_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='forest_designs.plant')),
                ('kind', models.ForeignKey(db_column='plantimagekind_uuid', on_delete=django.db.models.deletion.PROTECT, to='forest_designs.plantimagekind', to_field='uuid')),
            ],
            options={
                'verbose_name': 'plant image',
                'verbose_name_plural': 'plant images',
                'ordering': ('plant', '-date'),
            },
        ),
        migrations.CreateModel(
            name='PlantLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime.now, help_text='Timestamp of the log entry.', verbose_name='date')),
                ('notes', models.TextField(verbose_name='notes')),
                ('plant', models.ForeignKey(db_column='plant_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='forest_designs.plant', to_field='uuid')),
                ('kind', models.ForeignKey(db_column='plantlogkind_uuid', on_delete=django.db.models.deletion.PROTECT, to='forest_designs.plantlogkind', to_field='uuid')),
            ],
            options={
                'verbose_name': 'plant log',
                'verbose_name_plural': 'plant logs',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PlantStateTransition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, help_text='Moment of state transition.', verbose_name='date')),
                ('plant', models.ForeignKey(db_column='plant_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='statetransitions', to='forest_designs.plant', to_field='uuid')),
                ('state', models.ForeignKey(db_column='state_uuid', help_text='State to transition to.', on_delete=django.db.models.deletion.PROTECT, related_name='transitions', to='forest_designs.plantstate', to_field='uuid')),
            ],
            options={
                'verbose_name': 'plant state transition',
                'verbose_name_plural': 'plant state transitions',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('area', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='area')),
                ('kind', models.ForeignKey(db_column='zonekind_uuid', on_delete=django.db.models.deletion.PROTECT, to='forest_designs.zonekind', to_field='uuid')),
            ],
            options={
                'verbose_name': 'zone',
                'verbose_name_plural': 'zones',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('species__isnull', False), ('genus__isnull', False), ('variety__isnull', False), _connector='OR'), name='forest_designs_plant_genus_species_variety_notnull'),
        ),
    ]
