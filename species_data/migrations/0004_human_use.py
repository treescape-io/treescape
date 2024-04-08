from django.db import migrations


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
    for human_use in human_uses:
        HumanUse.objects.create(**human_use)


class Migration(migrations.Migration):
    dependencies = [
        ("species_data", "0003_growth_habits"),
    ]
    operations = [
        migrations.RunPython(create_human_uses),
    ]
