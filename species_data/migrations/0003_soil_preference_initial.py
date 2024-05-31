from django.db import migrations
from django.utils.text import slugify


def create_soil_preferences(apps, schema_editor):
    SoilPreference = apps.get_model("species_data", "SoilPreference")
    soil_preferences = [
        {
            "name": "Sandy",
            "description": "Soil with a gritty texture, good drainage but low nutrient and water retention.",
        },
        {
            "name": "Loamy",
            "description": "Soil with a balanced mix of sand, silt, and clay, offering good drainage, nutrient availability, and moisture retention.",
        },
        {
            "name": "Clayey",
            "description": "Soil with fine particles, high water retention, and nutrient levels but poor drainage.",
        },
        {
            "name": "Silty",
            "description": "Soil with fine particles that retain moisture and nutrients well but may have poor drainage.",
        },
        {
            "name": "Peaty",
            "description": "Soil high in organic matter, retaining moisture well but may be acidic.",
        },
        {
            "name": "Chalky",
            "description": "Alkaline soil with high calcium carbonate content, often stony and free-draining.",
        },
        {
            "name": "Saline",
            "description": "Soil with high salt content, usually found in arid or coastal areas.",
        },
    ]

    for preference in soil_preferences:
        preference["slug"] = slugify(preference["name"])
        obj = SoilPreference(**preference)
        obj.full_clean()
        obj.save()


def delete_soil_preferences(apps, schema_editor):
    SoilPreference = apps.get_model("species_data", "SoilPreference")
    SoilPreference.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("species_data", "0002_initial_data"),
    ]

    operations = [
        migrations.RunPython(create_soil_preferences, delete_soil_preferences),
    ]
