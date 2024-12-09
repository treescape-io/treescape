# Generated by Django 5.0.4 on 2024-05-29 18:09

from django.db import migrations
from django.template.defaultfilters import slugify


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

    for obj in climate_zones:
        obj["slug"] = slugify(obj["name"])
        created_obj = ClimateZone(**obj)
        created_obj.full_clean()
        created_obj.save()


def create_initial_growth_habits(apps, schema_editor):
    GrowthHabit = apps.get_model("species_data", "GrowthHabit")
    growth_habits = [
        {
            "name": "Tree",
            "description": "A woody perennial plant with a single main stem or trunk.",
        },
        {
            "name": "Shrub",
            "description": "A woody plant with multiple stems and shorter height than a tree.",
        },
        {"name": "Herb", "description": "A non-woody plant with soft, green stems."},
        {
            "name": "Vine",
            "description": "A climbing or trailing plant with long, slender stems.",
        },
        {
            "name": "Grass",
            "description": "A monocotyledonous plant with narrow leaves and hollow stems.",
        },
        {"name": "Fern", "description": "A flowerless, spore-bearing vascular plant."},
        {
            "name": "Moss",
            "description": "A small, non-vascular plant that grows in dense green clumps.",
        },
    ]

    for obj in growth_habits:
        obj["slug"] = slugify(str(obj["name"]))
        created_obj = GrowthHabit(**obj)
        created_obj.full_clean()
        created_obj.save()


def create_human_uses(apps, schema_editor):
    HumanUse = apps.get_model("species_data", "HumanUse")
    human_uses = [
        {
            "name": "Edible Fruits",
            "description": "The plant produces edible fruits that can be consumed by humans. Fruits provide nutritional value and can contribute to food security and income generation.",
            "use_type": "food",
        },
        {
            "name": "Edible Nuts",
            "description": "The plant produces edible nuts that are nutritious and can be consumed raw or processed. Nuts are a valuable food source and can have commercial value.",
            "use_type": "food",
        },
        {
            "name": "Edible Seeds",
            "description": "The seeds of the plant are edible and can be used in various culinary applications. Edible seeds can provide nutrition and have cultural significance.",
            "use_type": "food",
        },
        {
            "name": "Edible Leaves",
            "description": "The leaves of the plant are edible and can be used in salads or cooked dishes. Edible leaves offer dietary diversity and can have cultural significance in traditional cuisines.",
            "use_type": "food",
        },
        {
            "name": "Honey Production",
            "description": "The plant provides nectar and pollen for bees, supporting honey production. Honey is a valuable food product with nutritional and medicinal properties.",
            "use_type": "food",
        },
        {
            "name": "Medicinal Roots",
            "description": "The roots of the plant have medicinal properties and can be used for various health benefits. Medicinal roots can support traditional healthcare practices.",
            "use_type": "medicinal",
        },
        {
            "name": "Medicinal Flowers",
            "description": "The flowers of the plant have medicinal properties and can be used for various health benefits. Medicinal flowers can offer unique therapeutic value.",
            "use_type": "medicinal",
        },
        {
            "name": "Medicinal Bark",
            "description": "The bark of the plant has medicinal properties and can be used for various health benefits. Medicinal bark can contribute to community health and have socio-economic value.",
            "use_type": "medicinal",
        },
        {
            "name": "Medicinal Leaves",
            "description": "The leaves of the plant have medicinal properties and can be used for various health benefits. Medicinal leaves can provide accessible healthcare options and support traditional knowledge.",
            "use_type": "medicinal",
        },
        {
            "name": "Timber",
            "description": "The plant provides valuable timber for construction and woodworking. Timber production can generate income and support local industries.",
            "use_type": "material",
        },
        {
            "name": "Animal Fodder",
            "description": "The plant can be used as fodder for livestock or other animals. Animal fodder supports animal husbandry and can provide supplementary income for farmers.",
            "use_type": "material",
        },
        {
            "name": "Firewood",
            "description": "The wood of the plant can be used as firewood for cooking and heating. Fuelwood is a vital resource for many households and can reduce dependence on fossil fuels.",
            "use_type": "material",
        },
        {
            "name": "Fiber",
            "description": "The plant provides fiber that can be used for making textiles, ropes, or other materials. Fiber production can support local crafts and industries.",
            "use_type": "material",
        },
        {
            "name": "Dye",
            "description": "The plant produces natural dyes that can be used for coloring textiles or other materials. Natural dyes have cultural and eco-friendly value.",
            "use_type": "material",
        },
        {
            "name": "Resin",
            "description": "The plant produces resin that can be used for various purposes, such as adhesives, varnishes, or incense. Resin production can have economic and cultural significance.",
            "use_type": "material",
        },
        {
            "name": "Ornamental Flowers",
            "description": "The plant produces beautiful flowers that are used for ornamental purposes. Ornamental flowers can enhance landscapes, have cultural significance, and contribute to eco-tourism.",
            "use_type": "ornamental",
        },
        {
            "name": "Ornamental Foliage",
            "description": "The plant has attractive foliage that is used for ornamental purposes. Ornamental foliage can beautify spaces and have aesthetic value.",
            "use_type": "ornamental",
        },
        {
            "name": "Ornamental Bark",
            "description": "The bark of the plant has an attractive appearance and is used for ornamental purposes. Ornamental bark can add visual interest to landscapes.",
            "use_type": "ornamental",
        },
        {
            "name": "Hedge",
            "description": "The plant can be used as a hedge or border plant for landscaping. Hedges provide structure, privacy, and can have ecological benefits.",
            "use_type": "ornamental",
        },
    ]

    for obj in human_uses:
        obj["slug"] = slugify(str(obj["name"]))
        created_obj = HumanUse(**obj)
        created_obj.full_clean()
        created_obj.save()


def create_ecological_roles(apps, schema_editor):
    EcologicalRole = apps.get_model("species_data", "EcologicalRole")
    ecological_roles = [
        {
            "name": "Nitrogen Fixation",
            "description": "The plant has the ability to fix atmospheric nitrogen in the soil, improving soil fertility and benefiting other plants.",
        },
        {
            "name": "Soil Erosion Control",
            "description": "The plant helps to stabilize the soil and prevent erosion, particularly in sloping or degraded landscapes.",
        },
        {
            "name": "Water Regulation",
            "description": "The plant contributes to the regulation of water flow and retention in the ecosystem, helping to maintain water balance.",
        },
        {
            "name": "Carbon Sequestration",
            "description": "The plant absorbs and stores carbon dioxide from the atmosphere, contributing to climate change mitigation.",
        },
        {
            "name": "Habitat Provision",
            "description": "The plant provides habitat and shelter for various wildlife species, promoting biodiversity conservation.",
        },
        {
            "name": "Pollinator Attraction",
            "description": "The plant attracts pollinators such as bees, butterflies, and birds, supporting pollination services in the ecosystem.",
        },
        {
            "name": "Pest and Disease Control",
            "description": "The plant possesses natural pest and disease resistance properties, helping to control the spread of harmful organisms.",
        },
        {
            "name": "Soil Quality Improvement",
            "description": "The plant contributes to the improvement of soil structure, fertility, and organic matter content.",
        },
        {
            "name": "Microclimate Regulation",
            "description": "The plant helps to regulate the microclimate by providing shade, reducing wind speed, and moderating temperature.",
        },
        {
            "name": "Nutrient Cycling",
            "description": "The plant plays a role in the cycling of nutrients within the ecosystem, contributing to the overall health and productivity.",
        },
        {
            "name": "Windbreak",
            "description": "The plant can be used as a windbreak to reduce wind speed and protect crops or structures, providing ecological benefits.",
        },
        {
            "name": "Shade Provision",
            "description": "The plant provides shade, creating favorable conditions for other species and regulating the understory environment.",
        },
        {
            "name": "Soil Moisture Retention",
            "description": "The plant helps to retain soil moisture, reducing water loss and improving water availability for other plants.",
        },
        {
            "name": "Weed Suppression",
            "description": "The plant has the ability to suppress the growth of weeds through allelopathic effects or by outcompeting them.",
        },
        {
            "name": "Soil Nutrient Accumulation",
            "description": "The plant accumulates and stores nutrients in its biomass, which can be released back into the soil upon decomposition.",
        },
    ]

    for obj in ecological_roles:
        obj["slug"] = slugify(str(obj["name"]))
        created_obj = EcologicalRole(**obj)
        created_obj.full_clean()
        created_obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("species_data", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_climate_zones),
        migrations.RunPython(create_initial_growth_habits),
        migrations.RunPython(create_human_uses),
        migrations.RunPython(create_ecological_roles),
    ]
