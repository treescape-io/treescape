# Generated by Django 5.0.3 on 2024-04-06 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forest_designs', '0001_initial'),
        ('plant_species', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plant',
            options={'verbose_name': 'plant', 'verbose_name_plural': 'plants'},
        ),
        migrations.AddField(
            model_name='plant',
            name='variety',
            field=models.ForeignKey(blank=True, help_text='When specified, species and genus are automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.speciesvariety'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='genus',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.genus'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='species',
            field=models.ForeignKey(blank=True, help_text='When specified, genus is automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.species'),
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('species__isnull', False), ('genus__isnull', False), ('variety__isnull', False), _connector='OR'), name='forest_designs_plant_genus_species_variety_notnull'),
        ),
    ]
