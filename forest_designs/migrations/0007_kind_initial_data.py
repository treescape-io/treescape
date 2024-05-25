from django.db import migrations


def create_zone_kinds(apps, schema_editor):
    ZoneKind = apps.get_model("forest_designs", "ZoneKind")

    zone_kinds = [
        {
            "name": "Land Use",
            "description": """These zones reflect the specific management practices, intensities, or strategies applied to different areas of the agroforestry system.
Examples of Management Zones could include:
Intensive Management: Areas that require frequent interventions, high inputs, or close monitoring, such as vegetable plots or orchards.
Extensive Management: Sections that are managed with minimal inputs or interventions, such as pastures or woodlands.
Agroforestry Practices: Zones defined by specific agroforestry techniques, such as alley cropping, silvopasture, or forest farming.
Buffer Zones: Areas designed to provide protection, reduce soil erosion, or enhance ecosystem services, such as riparian buffers or windbreaks.""",
        },
        {
            "name": "Management Style",
            "description": """These zones reflect the specific management practices, intensities, or strategies applied to different areas of the agroforestry system.
Examples of Management Zones could include:
Intensive Management: Areas that require frequent interventions, high inputs, or close monitoring, such as vegetable plots or orchards.
Extensive Management: Sections that are managed with minimal inputs or interventions, such as pastures or woodlands.
Agroforestry Practices: Zones defined by specific agroforestry techniques, such as alley cropping, silvopasture, or forest farming.
Buffer Zones: Areas designed to provide protection, reduce soil erosion, or enhance ecosystem services, such as riparian buffers or windbreaks.""",
        },
    ]

    for kind in zone_kinds:
        ZoneKind.objects.create(name=kind["name"], description=kind["description"])


def reverse_create_zone_kinds(apps, schema_editor):
    ZoneKind = apps.get_model("forest_designs", "ZoneKind")
    ZoneKind.objects.all().delete()


def create_image_kinds(apps, schema_editor):
    ImageKind = apps.get_model("forest_designs", "PlantImageKind")

    image_kinds = [
        {
            "name": "Full Plant",
            "description": "Images showing the entire plant or tree in its habitat, providing an overview of its shape, size, and general appearance.",
        },
        {
            "name": "Leaves",
            "description": "Detailed images focusing on the leaves of the plant, showcasing their shape, size, color, and any distinguishing features.",
        },
        {
            "name": "Flowers",
            "description": "Images capturing the plant's flowers, including their color, shape, and arrangement.",
        },
        {
            "name": "Fruit or Seed",
            "description": "Images of the plant's fruits or seeds, aiding in identification, assessing ripeness, and monitoring yield.",
        },
        {
            "name": "Bark",
            "description": "Images highlighting the texture, color, and unique patterns of the tree's bark.",
        },
        {
            "name": "Pests or Diseases",
            "description": "Images documenting any visible signs of pests or diseases affecting the plant, such as leaf damage, discoloration, or the presence of insects.",
        },
        {
            "name": "Labels or Tags",
            "description": "Images of any labels, tags, or plant passports associated with the plant, including identification numbers, species names, or other relevant information.",
        },
    ]

    for image_kind in image_kinds:
        ImageKind.objects.create(
            name=image_kind["name"], description=image_kind["description"]
        )


def reverse_create_image_kinds(apps, schema_editor):
    ImageKind = apps.get_model("forest_designs", "PlantImageKind")
    ImageKind.objects.all().delete()


def create_plant_log_kinds(apps, schema_editor):
    PlantLogKind = apps.get_model("forest_designs", "PlantLogKind")

    plant_log_kinds = [
        {
            "name": "Planting & Establishment",
            "description": "Activities related to planting new trees or plants, including site preparation, planting techniques, and initial care.",
        },
        {
            "name": "Maintenance & Care",
            "description": "Ongoing activities to maintain plant health, such as pruning, weeding, mulching, and general upkeep.",
        },
        {
            "name": "Nutrient Management",
            "description": "Activities related to maintaining soil fertility and plant nutrition, such as fertilization, soil amendments, and composting.",
        },
        {
            "name": "Pest & Disease Management",
            "description": "Monitoring and managing pests and diseases that may affect plant health, including the use of integrated pest management techniques.",
        },
        {
            "name": "Irrigation & Water Management",
            "description": "Activities related to managing water resources, such as irrigation scheduling, water conservation techniques, and drainage.",
        },
        {
            "name": "Harvest & Yield",
            "description": "Activities related to harvesting crops, fruits, or other plant products, as well as recording yields and quality.",
        },
        {
            "name": "Observations & Monitoring",
            "description": "General observations and monitoring of plant growth, health, and ecosystem interactions, such as wildlife sightings or notable weather events.",
        },
    ]

    for plant_log_kind in plant_log_kinds:
        PlantLogKind.objects.create(
            name=plant_log_kind["name"], description=plant_log_kind["description"]
        )


def reverse_create_plant_log_kinds(apps, schema_editor):
    PlantLogKind = apps.get_model("forest_designs", "PlantLogKind")
    PlantLogKind.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "forest_designs",
            "0006_plantimagekind_description_plantlogkind_description_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(create_zone_kinds, reverse_create_zone_kinds),
        migrations.RunPython(create_plant_log_kinds, reverse_create_plant_log_kinds),
        migrations.RunPython(create_image_kinds, reverse_create_image_kinds),
    ]
