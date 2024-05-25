from unittest.mock import patch
from django.test import TestCase
from django.utils.text import slugify

from plant_species.models import Family, Genus, Species, SpeciesVariety


class SpeciesTestMixin:
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.family = Family.objects.create(latin_name="Rosaceae", gbif_id=1)
        cls.genus = Genus.objects.create(
            latin_name="Rosa", gbif_id=2, family=cls.family
        )
        cls.species = Species.objects.create(
            latin_name="Rosa rubiginosa", gbif_id=3, genus=cls.genus
        )
        cls.variety = SpeciesVariety.objects.create(
            name="TestVariety", species=cls.species
        )


class SpeciesBaseTestCase(SpeciesTestMixin, TestCase):
    def test_family_save(self):
        self.family.save()
        assert self.family.latin_name
        self.assertEqual(self.family.slug, slugify(self.family.latin_name))

    def test_genus_save(self):
        self.genus.save()
        assert self.genus.latin_name
        self.assertEqual(self.genus.slug, slugify(self.genus.latin_name))

    def test_species_save(self):
        self.species.save()
        assert self.species.latin_name
        self.assertEqual(self.species.slug, slugify(self.species.latin_name))

    @patch("plant_species.models.get_latin_names")
    def test_enrich_gbif_backbone(self, mock_get_latin_names):
        mock_get_latin_names.return_value = {
            "speciesKey": 4,
            "genusKey": 5,
            "familyKey": 6,
            "species": "Rosb rubiginosb",
            "genus": "Rosb",
            "family": "Rosaceab",
        }

        new_species = Species(latin_name="Banana bananinus")
        new_species.enrich_gbif_backbone()

        self.assertEqual(new_species.latin_name, "Rosb rubiginosb")
        self.assertEqual(new_species.gbif_id, 4)
        self.assertIsNotNone(new_species.genus)
        self.assertEqual(new_species.genus.latin_name, "Rosb")
        self.assertEqual(new_species.genus.gbif_id, 5)
        self.assertIsNotNone(new_species.genus.family)
        self.assertEqual(new_species.genus.family.latin_name, "Rosaceab")
        self.assertEqual(new_species.genus.family.gbif_id, 6)

        # This should not cause any errors.
        new_species.save()
