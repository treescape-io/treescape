from django.db import migrations


def create_climate_zones(apps, schema_editor):
    ClimateZone = apps.get_model("species_data", "ClimateZone")
    climate_zones = [
        {
            "main_group": "A",
            "seasonal_precipitation": "f",
            "heat_level": None,
            "name": "Tropical rainforest climate",
            "description": "Average precipitation of at least 60 mm in every month.",
        },
        {
            "main_group": "A",
            "seasonal_precipitation": "m",
            "heat_level": None,
            "name": "Tropical monsoon climate",
            "description": "Driest month with precipitation less than 60 mm, but at least 100 - (Total Annual Precipitation (mm) / 25).",
        },
        {
            "main_group": "A",
            "seasonal_precipitation": "w",
            "heat_level": None,
            "name": "Tropical wet and dry or savanna climate (dry winter)",
            "description": "Driest month having precipitation less than 60 mm and less than 100 - (Total Annual Precipitation (mm) / 25).",
        },
        {
            "main_group": "A",
            "seasonal_precipitation": "s",
            "heat_level": None,
            "name": "Tropical wet and dry or savanna climate (dry summer)",
            "description": "Driest month having precipitation less than 60 mm and less than 100 - (Total Annual Precipitation (mm) / 25).",
        },
        {
            "main_group": "B",
            "seasonal_precipitation": "W",
            "heat_level": "h",
            "name": "Hot desert climate",
            "description": "Annual precipitation less than 50% of the threshold for a desert climate.",
        },
        {
            "main_group": "B",
            "seasonal_precipitation": "W",
            "heat_level": "k",
            "name": "Cold desert climate",
            "description": "Annual precipitation less than 50% of the threshold for a desert climate.",
        },
        {
            "main_group": "B",
            "seasonal_precipitation": "S",
            "heat_level": "h",
            "name": "Hot semi-arid climate",
            "description": "Annual precipitation between 50% and 100% of the threshold for a desert climate.",
        },
        {
            "main_group": "B",
            "seasonal_precipitation": "S",
            "heat_level": "k",
            "name": "Cold semi-arid climate",
            "description": "Annual precipitation between 50% and 100% of the threshold for a desert climate.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "f",
            "heat_level": "a",
            "name": "Humid subtropical climate",
            "description": "Coldest month averaging above 0°C, at least one month's average temperature above 22°C, and at least four months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "f",
            "heat_level": "b",
            "name": "Temperate oceanic climate or subtropical highland climate",
            "description": "Coldest month averaging above 0°C, all months with average temperatures below 22°C, and at least four months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "f",
            "heat_level": "c",
            "name": "Subpolar oceanic climate",
            "description": "Coldest month averaging above 0°C and 1-3 months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "w",
            "heat_level": "a",
            "name": "Monsoon-influenced humid subtropical climate",
            "description": "Coldest month averaging above 0°C, at least one month's average temperature above 22°C, and at least four months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "w",
            "heat_level": "b",
            "name": "Subtropical highland climate or Monsoon-influenced temperate oceanic climate",
            "description": "Coldest month averaging above 0°C, all months with average temperatures below 22°C, and at least four months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "w",
            "heat_level": "c",
            "name": "Cold subtropical highland climate or Monsoon-influenced subpolar oceanic climate",
            "description": "Coldest month averaging above 0°C and 1-3 months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "s",
            "heat_level": "a",
            "name": "Hot-summer Mediterranean climate",
            "description": "Coldest month averaging above 0°C, at least one month's average temperature above 22°C, and at least four months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 40 mm.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "s",
            "heat_level": "b",
            "name": "Warm-summer Mediterranean climate",
            "description": "Coldest month averaging above 0°C, all months with average temperatures below 22°C, and at least four months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 40 mm.",
        },
        {
            "main_group": "C",
            "seasonal_precipitation": "s",
            "heat_level": "c",
            "name": "Cold-summer Mediterranean climate",
            "description": "Coldest month averaging above 0°C and 1-3 months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 40 mm.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "f",
            "heat_level": "a",
            "name": "Hot-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, at least one month's average temperature above 22°C, and at least four months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "f",
            "heat_level": "b",
            "name": "Warm-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, all months with average temperatures below 22°C, and at least four months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "f",
            "heat_level": "c",
            "name": "Subarctic climate",
            "description": "Coldest month averaging below 0°C and 1-3 months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "f",
            "heat_level": "d",
            "name": "Extremely cold subarctic climate",
            "description": "Coldest month averaging below -38°C and 1-3 months averaging above 10°C. No significant precipitation difference between seasons.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "w",
            "heat_level": "a",
            "name": "Monsoon-influenced hot-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, at least one month's average temperature above 22°C, and at least four months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "w",
            "heat_level": "b",
            "name": "Monsoon-influenced warm-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, all months with average temperatures below 22°C, and at least four months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "w",
            "heat_level": "c",
            "name": "Monsoon-influenced subarctic climate",
            "description": "Coldest month averaging below 0°C and 1-3 months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "w",
            "heat_level": "d",
            "name": "Monsoon-influenced extremely cold subarctic climate",
            "description": "Coldest month averaging below -38°C and 1-3 months averaging above 10°C. At least ten times as much rain in the wettest month of summer as in the driest month of winter.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "s",
            "heat_level": "a",
            "name": "Mediterranean-influenced hot-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, average temperature of the warmest month above 22°C and at least four months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 30 mm.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "s",
            "heat_level": "b",
            "name": "Mediterranean-influenced warm-summer humid continental climate",
            "description": "Coldest month averaging below 0°C, average temperature of the warmest month below 22°C and at least four months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 30 mm.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "s",
            "heat_level": "c",
            "name": "Mediterranean-influenced subarctic climate",
            "description": "Coldest month averaging below 0°C and 1-3 months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 30 mm.",
        },
        {
            "main_group": "D",
            "seasonal_precipitation": "s",
            "heat_level": "d",
            "name": "Mediterranean-influenced extremely cold subarctic climate",
            "description": "Coldest month averaging below -38°C and 1-3 months averaging above 10°C. At least three times as much precipitation in the wettest month of winter as in the driest month of summer, and the driest month of summer receives less than 30 mm.",
        },
        {
            "main_group": "E",
            "seasonal_precipitation": None,
            "heat_level": "T",
            "name": "Tundra climate",
            "description": "Average temperature of warmest month between 0°C and 10°C.",
        },
        {
            "main_group": "E",
            "seasonal_precipitation": None,
            "heat_level": "F",
            "name": "Ice cap climate",
            "description": "Eternal winter, with all 12 months of the year with average temperatures below 0°C.",
        },
    ]

    for zone in climate_zones:
        ClimateZone.objects.create(**zone)


def remove_climate_zones(apps, schema_editor):
    ClimateZone = apps.get_model("species_data", "ClimateZone")
    ClimateZone.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("species_data", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_climate_zones, remove_climate_zones),
    ]
