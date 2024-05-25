from django.test import TestCase

from forest_designs.models import Plant, PlantImage, PlantLog
from plant_species.models import Genus, Species, SpeciesVariety, Family


class PlantTestCase(TestCase):
    """Test all methods on Plant."""

    def test_clean_method(self):
        """Test the clean method of Plant model."""

        family = Family.objects.create(latin_name="TestFamily", gbif_id=1)
        genus = Genus.objects.create(latin_name="TestGenus", gbif_id=2, family=family)
        species = Species.objects.create(latin_name="TestSpecies", genus=genus, gbif_id=3)
        variety = SpeciesVariety.objects.create(name="TestVariety", species=species)

        plant = Plant(variety=variety, location="POINT(0 0)")
        plant.clean()

        self.assertEqual(plant.species, species)
        self.assertEqual(plant.genus, genus)
