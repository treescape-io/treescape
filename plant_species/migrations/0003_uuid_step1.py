# Generated by Django 5.0.4 on 2024-12-02 22:07

from django.db import migrations
import uuid


def set_uuids(apps, schema_editor):
    models = [
        "Family",
        "FamilyCommonName",
        "Genus",
        "GenusCommonName",
        "Species",
        "SpeciesCommonName",
        "SpeciesVariety",
    ]

    for model_name in models:
        Model = apps.get_model("plant_species", model_name)
        for instance in Model.objects.all():
            instance.uuid = uuid.uuid4()
            instance.save(update_fields=["uuid"])


def reverse_uuids(apps, schema_editor):
    pass  # Cannot meaningfully reverse UUID assignment


class Migration(migrations.Migration):
    dependencies = [
        ("plant_species", "0002_family_uuid_familycommonname_uuid_genus_uuid_and_more"),
    ]

    operations = [
        migrations.RunPython(set_uuids, reverse_uuids),
    ]