# Generated by Django 5.0.4 on 2025-01-03 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forest_designs", "0004_alter_plantimage_plant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="genus",
            field=models.ForeignKey(
                blank=True,
                db_column="genus_uuid",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="plant_species.genus",
                to_field="uuid",
            ),
        ),
    ]
