from django.test import TestCase
from django.core.exceptions import ValidationError

from forest_designs.models import Plant, PlantImage, PlantLog
from plant_species.models import Genus, Species, SpeciesVariety, Family


class PlantTestCase(TestCase):
    """Test all methods on Plant."""

    def test_clean_method(self):
        """Test the clean method of Plant model."""

        family = Family.objects.create(latin_name="TestFamily", gbif_id=1)
        genus = Genus.objects.create(latin_name="TestGenus", gbif_id=2, family=family)
        species = Species.objects.create(
            latin_name="TestSpecies", genus=genus, gbif_id=3
        )
        variety = SpeciesVariety.objects.create(name="TestVariety", species=species)

        plant = Plant(variety=variety, location="POINT(0 0)")
        plant.clean()

        self.assertEqual(plant.species, species)
        self.assertEqual(plant.genus, genus)

    def test_get_name_method(self):
        """Test the get_name method of Plant model."""

        family = Family.objects.create(latin_name="TestFamily1", gbif_id=1)
        genus = Genus.objects.create(latin_name="TestGenus1", gbif_id=2, family=family)
        species = Species.objects.create(
            latin_name="TestSpecies1", genus=genus, gbif_id=3
        )
        variety = SpeciesVariety.objects.create(name="TestVariety1", species=species)

        # Test with variety
        plant = Plant(variety=variety, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(variety))

        # Test with species
        plant = Plant(species=species, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(species))

        # Test with genus
        plant = Plant(genus=genus, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(genus))

        # Test with no variety, species, or genus
        plant = Plant(location="POINT(0 0)")
        self.assertIsNone(plant.get_name())
        """Test the clean method of Plant model."""

        family = Family.objects.create(latin_name="TestFamily2", gbif_id=4)
        genus = Genus.objects.create(latin_name="TestGenus2", gbif_id=5, family=family)
        species = Species.objects.create(
            latin_name="TestSpecies2", genus=genus, gbif_id=6
        )
        variety = SpeciesVariety.objects.create(name="TestVariety2", species=species)

        plant = Plant(variety=variety, location="POINT(0 0)")
        plant.clean()

        self.assertEqual(plant.species, species)
        self.assertEqual(plant.genus, genus)

    def test_constraints(self):
        """Test the constraints on the Plant model."""

        family = Family.objects.create(latin_name="TestFamily3", gbif_id=7)
        genus = Genus.objects.create(latin_name="TestGenus3", gbif_id=8, family=family)
        species = Species.objects.create(
            latin_name="TestSpecies3", genus=genus, gbif_id=9
        )
        variety = SpeciesVariety.objects.create(name="TestVariety3", species=species)

        # Test with no species, genus, or variety
        plant = Plant(location="POINT(0 0)")
        with self.assertRaises(ValidationError):
            plant.full_clean()

        # Test with genus only
        plant = Plant(genus=genus, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")

        # Test with species only
        plant = Plant(species=species, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")

        # Test with variety only
        plant = Plant(variety=variety, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")
