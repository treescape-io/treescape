from django.db import migrations


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
    for ecological_role in ecological_roles:
        EcologicalRole.objects.create(**ecological_role)


class Migration(migrations.Migration):
    dependencies = [
        ("species_data", "0004_human_use"),
    ]
    operations = [
        migrations.RunPython(create_ecological_roles),
    ]
