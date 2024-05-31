from django.db import migrations
from django.utils.text import slugify


def create_propagation_methods(apps, schema_editor):
    PropagationMethod = apps.get_model("species_data", "PropagationMethod")
    propagation_methods = [
        {
            "name": "Seed Propagation",
            "description": "Propagation through the sowing of seeds. Includes direct seeding and seedling transplants.",
        },
        {
            "name": "Cuttings",
            "description": "Vegetative propagation method using parts of plants (softwood, hardwood, semi-hardwood cuttings) to grow new plants.",
        },
        {
            "name": "Layering",
            "description": "Propagation technique where a branch is encouraged to form roots while still attached to the parent plant. Includes air layering and ground layering.",
        },
        {
            "name": "Grafting",
            "description": "Joining parts of two plants so that they grow as one. Includes cleft grafting, bud grafting, and whip and tongue grafting.",
        },
        {
            "name": "Division",
            "description": "Propagation by dividing the root, rhizome, tuber, or other parts of the plant into sections that each become new plants.",
        },
        {
            "name": "Micropropagation (Tissue Culture)",
            "description": "Propagation of plants by growing plant cells, tissues, or organs in a sterile environment on a nutrient culture medium.",
        },
        {
            "name": "Suckering",
            "description": "Propagation through new shoots that grow from the base or roots of the parent plant.",
        },
        {
            "name": "Stoloniferous Propagation",
            "description": "Propagation using stolons, which are horizontal above-ground stems that produce new plants at the nodes.",
        },
        {
            "name": "Rhizomatous Propagation",
            "description": "Propagation using rhizomes, which are horizontal underground stems that produce new plants.",
        },
        {
            "name": "Bulb and Tuber Propagation",
            "description": "Propagation using bulbs or tubers, such as those of onions, garlic, and potatoes.",
        },
    ]

    for method in propagation_methods:
        method["slug"] = slugify(method["name"])
        obj = PropagationMethod(**method)
        obj.full_clean()
        obj.save()


def delete_propagation_methods(apps, schema_editor):
    PropagationMethod = apps.get_model("species_data", "PropagationMethod")
    PropagationMethod.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "species_data",
            "0004_propagationmethod_remove_humanusethroughbase_source_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(create_propagation_methods, delete_propagation_methods),
    ]
