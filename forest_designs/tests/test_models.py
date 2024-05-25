from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError

from forest_designs.models import Plant, PlantImage, PlantLog, PlantLogType
from plant_species.tests.test_models import SpeciesTestMixin


class PlantTestCase(SpeciesTestMixin, TestCase):
    """Test all methods on Plant."""

    def test_get_name_method(self):
        """Test the get_name method of Plant model."""

        # Test with variety
        plant = Plant(variety=self.variety, genus=self.genus, location="POINT(0 0)")
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

    def test_save_plant_log(self):
        """Test the save method of PlantLog model."""

        plant = Plant(variety=self.variety, location="POINT(0 0)")
        plant.save()

        log_type = PlantLogType.objects.create(name="Test Log Type")
        plant_log = PlantLog(plant=plant, log_type=log_type, notes="Test log entry")
        plant_log.save()

        saved_plant_log = PlantLog.objects.get(id=plant_log.pk)
        self.assertEqual(saved_plant_log.notes, "Test log entry")
        self.assertEqual(saved_plant_log.plant, plant)
