from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError

from forest_designs.models import Plant, PlantImage, PlantLog
from plant_species.models import Genus, Species, SpeciesVariety, Family


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


class PlantTestCase(SpeciesTestMixin, TestCase):
    """Test all methods on Plant."""

    def test_clean_method(self):
        """Test the clean method of Plant model."""

        plant = Plant(variety=self.variety, location="POINT(0 0)")
        plant.clean()

        self.assertEqual(plant.species, self.species)
        self.assertEqual(plant.genus, self.genus)

    def test_get_name_method(self):
        """Test the get_name method of Plant model."""

        # Test with variety
        plant = Plant(variety=self.variety, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(self.variety))

        # Test with species
        plant = Plant(species=self.species, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(self.species))

        # Test with genus
        plant = Plant(genus=self.genus, location="POINT(0 0)")
        self.assertEqual(plant.get_name(), str(self.genus))

        # Test with no variety, species, or genus
        plant = Plant(location="POINT(0 0)")
        self.assertIsNone(plant.get_name())

    def test_save_method(self):
        """Test the save method of Plant model."""

        # Test save with variety
        plant = Plant(
            variety=self.variety,
            species=self.species,
            genus=self.genus,
            location="POINT(0 0)",
        )
        plant.save()

        plant = Plant.objects.get(id=plant.pk)
        self.assertEqual(plant.species, self.species)
        self.assertEqual(plant.genus, self.genus)

        # Test save with no variety, species, or genus
        plant = Plant(location="POINT(3 3)")
        with self.assertRaises(IntegrityError):
            plant.save()

    def test_constraints(self):
        """Test the constraints on the Plant model."""

        # Test with no species, genus, or variety
        plant = Plant(location="POINT(0 0)")
        with self.assertRaises(ValidationError):
            plant.full_clean()

        # Test with genus only
        plant = Plant(genus=self.genus, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")

        # Test with species only
        plant = Plant(species=self.species, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")

        # Test with variety only
        plant = Plant(variety=self.variety, location="POINT(0 0)")
        try:
            plant.clean()
        except ValidationError:
            self.fail("Plant.clean() raised ValidationError unexpectedly!")
