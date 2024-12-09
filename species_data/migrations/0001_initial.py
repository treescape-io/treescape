# Generated by Django 5.0.4 on 2024-12-09 14:43

import datetime
import django.core.validators
import django.db.models.deletion
import species_data.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant_species', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcologicalRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'ecological role',
                'verbose_name_plural': 'ecological roles',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GrowthHabit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'growth habit',
                'verbose_name_plural': 'growth habits',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HumanUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField()),
                ('use_type', models.CharField(choices=[('food', 'Food'), ('medicinal', 'Medicinal'), ('material', 'Material'), ('ornamental', 'Ornamental'), ('other', 'Other')], db_index=True, max_length=16, verbose_name='use type')),
            ],
            options={
                'verbose_name': 'human use',
                'verbose_name_plural': 'human uses',
                'ordering': ('use_type', 'name'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropagationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='Optional description of propagation method.', verbose_name='description')),
            ],
            options={
                'verbose_name': 'propagation method',
                'verbose_name_plural': 'propagation methods',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoilPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='Optional description of soil preference.', verbose_name='description')),
            ],
            options={
                'verbose_name': 'soil texture',
                'verbose_name_plural': 'soil textures',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'source type',
                'verbose_name_plural': 'source types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ClimateZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField()),
                ('main_group', models.CharField(choices=[('A', 'A: Tropical'), ('B', 'B: Dry'), ('C', 'C: Temperate'), ('D', 'D: Continental'), ('E', 'E: Polar')], max_length=1, verbose_name='main group')),
                ('seasonal_precipitation', models.CharField(blank=True, choices=[('S', 'S: Semi-Arid or steppe'), ('W', 'W: Arid Desert'), ('f', 'f: No dry season'), ('m', 'm: Monsoon'), ('w', 'w: Wet winter'), ('s', 's: Wet summer')], max_length=1, null=True, verbose_name='seasonal precipitation')),
                ('heat_level', models.CharField(blank=True, choices=[('h', 'h: Hot arid'), ('k', 'k: Cold arid'), ('a', 'a: Hot summer'), ('b', 'b: Warm summer'), ('c', 'c: Cool summer'), ('d', 'd: Very cold winter'), ('T', 'T: Tundra'), ('F', 'F: Ice cap')], max_length=1, null=True, verbose_name='heat level')),
            ],
            options={
                'verbose_name': 'climate zone',
                'verbose_name_plural': 'climate zones',
                'ordering': ('main_group', 'seasonal_precipitation', 'heat_level'),
                'abstract': False,
                'unique_together': {('main_group', 'seasonal_precipitation', 'heat_level')},
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='date')),
                ('url', models.URLField(unique=True, verbose_name='URL')),
                ('source_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='species_data.sourcetype')),
            ],
            options={
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpeciesClimateZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('climate_zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.climatezone')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeciesEcologicalRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('ecological_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.ecologicalrole')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeciesGrowthHabit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('growth_habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.growthhabit')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeciesHumanUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('human_use', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.humanuse')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeciesPropagationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('propagation_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.propagationmethod')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeciesProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height_minimum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('height_typical', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('height_maximum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('height_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('width_minimum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('width_typical', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('width_maximum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('width_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('soil_acidity_minimum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('soil_acidity_typical', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('soil_acidity_maximum', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('soil_acidity_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('sun_hours_minimum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('sun_hours_typical', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('sun_hours_maximum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('sun_hours_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('production_start_minimum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('production_start_typical', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('production_start_maximum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('production_start_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('production_peak_minimum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('production_peak_typical', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('production_peak_maximum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('production_peak_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('lifetime_minimum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s minimum')),
                ('lifetime_typical', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s typical')),
                ('lifetime_maximum', models.DurationField(blank=True, null=True, verbose_name='%(parent_verbose_name)s maximum')),
                ('lifetime_confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='%(parent_verbose_name)s confidence')),
                ('climate_zones', models.ManyToManyField(through='species_data.SpeciesClimateZone', to='species_data.climatezone')),
                ('ecological_roles', models.ManyToManyField(through='species_data.SpeciesEcologicalRole', to='species_data.ecologicalrole')),
                ('growth_habits', models.ManyToManyField(through='species_data.SpeciesGrowthHabit', to='species_data.growthhabit')),
                ('height_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('human_uses', models.ManyToManyField(through='species_data.SpeciesHumanUse', to='species_data.humanuse')),
                ('lifetime_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('production_peak_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('production_start_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('propagation_methods', models.ManyToManyField(through='species_data.SpeciesPropagationMethod', to='species_data.propagationmethod')),
                ('soil_acidity_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('species', models.OneToOneField(db_column='species_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='plant_species.species')),
                ('sun_hours_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
                ('width_source', species_data.fields.SourceField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='species_data.source', verbose_name='%(parent_verbose_name)s source')),
            ],
            options={
                'verbose_name': 'species properties',
                'verbose_name_plural': 'species properties',
            },
        ),
        migrations.AddField(
            model_name='speciespropagationmethod',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties'),
        ),
        migrations.AddField(
            model_name='specieshumanuse',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties'),
        ),
        migrations.AddField(
            model_name='speciesgrowthhabit',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties'),
        ),
        migrations.AddField(
            model_name='speciesecologicalrole',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties'),
        ),
        migrations.AddField(
            model_name='speciesclimatezone',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties'),
        ),
        migrations.CreateModel(
            name='SpeciesSoilPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', species_data.fields.ConfidenceField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='confidence')),
                ('soil_texture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.soilpreference')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.source')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='species_data.speciesproperties')),
            ],
            options={
                'abstract': False,
                'unique_together': {('species', 'soil_texture')},
            },
        ),
        migrations.AddField(
            model_name='speciesproperties',
            name='soil_preferences',
            field=models.ManyToManyField(through='species_data.SpeciesSoilPreference', to='species_data.soilpreference'),
        ),
        migrations.AlterUniqueTogether(
            name='speciespropagationmethod',
            unique_together={('species', 'propagation_method')},
        ),
        migrations.AlterUniqueTogether(
            name='specieshumanuse',
            unique_together={('species', 'human_use')},
        ),
        migrations.AlterUniqueTogether(
            name='speciesgrowthhabit',
            unique_together={('species', 'growth_habit')},
        ),
        migrations.AlterUniqueTogether(
            name='speciesecologicalrole',
            unique_together={('species', 'ecological_role')},
        ),
        migrations.AlterUniqueTogether(
            name='speciesclimatezone',
            unique_together={('species', 'climate_zone')},
        ),
    ]
