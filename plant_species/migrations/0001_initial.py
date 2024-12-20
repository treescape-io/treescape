# Generated by Django 5.0.4 on 2024-12-20 17:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('latin_name', models.CharField(blank=True, max_length=255, unique=True, verbose_name='latin name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('gbif_id', models.IntegerField(editable=False, unique=True, verbose_name='GBIF usageKey')),
                ('image', models.ImageField(blank=True, null=True, upload_to='plant_species/images/')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/thumbnails/')),
                ('image_large', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/large/')),
            ],
            options={
                'verbose_name': 'family',
                'verbose_name_plural': 'families',
                'ordering': ['latin_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('latin_name', models.CharField(blank=True, max_length=255, unique=True, verbose_name='latin name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('gbif_id', models.IntegerField(editable=False, unique=True, verbose_name='GBIF usageKey')),
                ('image', models.ImageField(blank=True, null=True, upload_to='plant_species/images/')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/thumbnails/')),
                ('image_large', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/large/')),
                ('family', models.ForeignKey(blank=True, db_column='family_uuid', on_delete=django.db.models.deletion.PROTECT, related_name='genera', to='plant_species.family', to_field='uuid')),
            ],
            options={
                'verbose_name': 'genus',
                'verbose_name_plural': 'genera',
                'ordering': ['latin_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('latin_name', models.CharField(blank=True, max_length=255, unique=True, verbose_name='latin name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('gbif_id', models.IntegerField(editable=False, unique=True, verbose_name='GBIF usageKey')),
                ('image', models.ImageField(blank=True, null=True, upload_to='plant_species/images/')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/thumbnails/')),
                ('image_large', models.ImageField(blank=True, editable=False, null=True, upload_to='plant_species/images/large/')),
                ('genus', models.ForeignKey(blank=True, db_column='genus_uuid', on_delete=django.db.models.deletion.PROTECT, related_name='species', to='plant_species.genus', to_field='uuid')),
            ],
            options={
                'verbose_name': 'species',
                'verbose_name_plural': 'species',
                'ordering': ['latin_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FamilyCommonName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('language', models.CharField(choices=[('pt', 'Portuguese'), ('nl', 'Dutch'), ('en', 'English'), ('es', 'Spanish')], max_length=7, verbose_name='language')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='common name')),
                ('is_default', models.BooleanField(default=False, help_text='Use as default name for language.', verbose_name='default')),
                ('family', models.ForeignKey(db_column='family_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='common_names', to='plant_species.family', to_field='uuid')),
            ],
            options={
                'verbose_name': 'common name',
                'verbose_name_plural': 'common names',
                'ordering': ['language', '-is_default', 'name'],
                'abstract': False,
                'unique_together': {('family', 'language', 'name')},
            },
        ),
        migrations.CreateModel(
            name='GenusCommonName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('language', models.CharField(choices=[('pt', 'Portuguese'), ('nl', 'Dutch'), ('en', 'English'), ('es', 'Spanish')], max_length=7, verbose_name='language')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='common name')),
                ('is_default', models.BooleanField(default=False, help_text='Use as default name for language.', verbose_name='default')),
                ('genus', models.ForeignKey(db_column='genus_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='common_names', to='plant_species.genus', to_field='uuid')),
            ],
            options={
                'verbose_name': 'common name',
                'verbose_name_plural': 'common names',
                'ordering': ['language', '-is_default', 'name'],
                'abstract': False,
                'unique_together': {('genus', 'language', 'name')},
            },
        ),
        migrations.CreateModel(
            name='SpeciesCommonName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('language', models.CharField(choices=[('pt', 'Portuguese'), ('nl', 'Dutch'), ('en', 'English'), ('es', 'Spanish')], max_length=7, verbose_name='language')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='common name')),
                ('is_default', models.BooleanField(default=False, help_text='Use as default name for language.', verbose_name='default')),
                ('species', models.ForeignKey(db_column='species_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='common_names', to='plant_species.species', to_field='uuid')),
            ],
            options={
                'verbose_name': 'common name',
                'verbose_name_plural': 'common names',
                'ordering': ['language', '-is_default', 'name'],
                'abstract': False,
                'unique_together': {('species', 'language', 'name')},
            },
        ),
        migrations.CreateModel(
            name='SpeciesVariety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='variety name')),
                ('species', models.ForeignKey(db_column='species_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='varieties', to='plant_species.species', to_field='uuid')),
            ],
            options={
                'verbose_name': 'variety',
                'verbose_name_plural': 'varieties',
                'ordering': ['species__latin_name', 'name'],
                'unique_together': {('species', 'name')},
            },
        ),
    ]
