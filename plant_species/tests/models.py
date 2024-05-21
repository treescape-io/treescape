from django.test import TestCase
from django.utils.text import slugify

from plant_species.models import Family, Genus, Species


class SpeciesBaseTestCase(TestCase):
    def test_family_save(self):
        family = Family.objects.create(latin_name="Rosaceae", gbif_id=1)
        family.save()
        assert family.latin_name
        self.assertEqual(family.slug, slugify(family.latin_name))

    def test_genus_save(self):
        family = Family.objects.create(latin_name="Rosaceae", gbif_id=1)
        genus = Genus.objects.create(latin_name="Rosa", gbif_id=2, family=family)
        genus.save()
        assert genus.latin_name
        self.assertEqual(genus.slug, slugify(genus.latin_name))

    def test_species_save(self):
        family = Family.objects.create(latin_name="Rosaceae", gbif_id=1)
        genus = Genus.objects.create(latin_name="Rosa", gbif_id=2, family=family)
        species = Species.objects.create(
            latin_name="Rosa rubiginosa", gbif_id=3, genus=genus
        )
        species.save()
        assert species.latin_name
        self.assertEqual(species.slug, slugify(species.latin_name))
