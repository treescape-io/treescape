# Generated by Django 5.0.4 on 2024-12-16 15:35

from django.db import migrations


def create_plant_states(apps, schema_editor):
    PlantState = apps.get_model("forest_designs", "PlantState")
    initial_states = [
        {
            "name": "Planned",
            "description": "The plant is included in the agroforestry design but has not been physically planted yet.",
        },
        {
            "name": "Planted",
            "description": "The plant has been physically planted in the designated location within the agroforestry system.",
        },
        {
            "name": "Native",
            "description": "The plant is a native species that naturally exists in the agroforestry site and has not been actively planted.",
        },
        {
            "name": "Dead",
            "description": "The plant has died and is no longer actively contributing to the agroforestry system.",
        },
        {
            "name": "Removed",
            "description": "The plant has been intentionally removed from the agroforestry system, including cases where it was cut down, due to various reasons (e.g., disease, overcrowding, end of life cycle, timber harvesting).",
        },
    ]
    for state_data in initial_states:
        PlantState.objects.create(**state_data)


class Migration(migrations.Migration):
    dependencies = [
        (
            "forest_designs",
            "0003_plantstate_remove_plant_notes_alter_plantlog_date_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(create_plant_states),
    ]
