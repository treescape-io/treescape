from django.db import IntegrityError
from django.test import TestCase

from forest_designs.models import (
    Plant,
    PlantImage,
    PlantLog,
    PlantLogKind,
    PlantImageKind,
)
from plant_species.tests.test_models import SpeciesTestMixin
from forest_designs.models import Zone, ZoneKind


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


class PlantLogTestCase(SpeciesTestMixin, TestCase):
    def test_save(self):
        """Test the save method of PlantLog model."""

        plant = Plant(variety=self.variety, location="POINT(0 0)")
        plant.save()

        kind = PlantLogKind.objects.create(name="Test Log Type")
        plant_log = PlantLog(plant=plant, kind=kind, notes="Test log entry")
        plant_log.save()

        saved_plant_log = PlantLog.objects.get(id=plant_log.pk)
        self.assertEqual(saved_plant_log.notes, "Test log entry")
        self.assertEqual(saved_plant_log.plant, plant)


class ImageTestCase(SpeciesTestMixin, TestCase):
    def test_save(self):
        """Test the save method of PlantImage model."""

        plant = Plant(variety=self.variety, location="POINT(0 0)")
        plant.save()

        kind = PlantImageKind.objects.create(name="Test Image Type")
        plant_image = PlantImage(
            plant=plant,
            kind=kind,
            date="2023-01-01T00:00:00Z",
            image="path/to/image.jpg",
        )
        plant_image.save()

        saved_plant_image = PlantImage.objects.get(id=plant_image.pk)
        self.assertEqual(saved_plant_image.plant, plant)
        self.assertEqual(saved_plant_image.kind, kind)
        self.assertEqual(
            saved_plant_image.date.isoformat(), "2023-01-01T00:00:00+00:00"
        )
        self.assertEqual(saved_plant_image.image, "path/to/image.jpg")


class ZoneTestCase(TestCase):
    def test_save(self):
        """Test the save method of Zone model."""

        zone_kind = ZoneKind.objects.create(name="Test Zone Type")
        zone = Zone(
            name="Test Zone", kind=zone_kind, area="MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))"
        )
        zone.save()

        saved_zone = Zone.objects.get(id=zone.pk)
        self.assertEqual(saved_zone.name, "Test Zone")
        self.assertEqual(saved_zone.kind, zone_kind)
        self.assertEqual(saved_zone.area.wkt, "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))")
