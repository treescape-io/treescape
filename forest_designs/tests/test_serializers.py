import json
from django.test import TestCase
from django.contrib.gis.geos import Point, MultiPolygon, Polygon
from forest_designs.models import Plant, Zone, ZoneKind, PlantState
from forest_designs.serializers import PlantGeoSerializer, ZoneGeoSerializer
from plant_species.tests.test_models import SpeciesTestMixin


class GeoSerializerTestCase(SpeciesTestMixin, TestCase):
    """Test case for the GeoJSON serializers."""
    
    def setUp(self):
        super().setUp()
        
        # Create zone
        self.zone_kind = ZoneKind.objects.create(name="Test Zone Kind")
        self.zone = Zone.objects.create(
            name="Test Zone",
            kind=self.zone_kind,
            area=MultiPolygon(Polygon.from_bbox((0, 0, 10, 10)))
        )
        
        # Create plant
        self.plant = Plant.objects.create(
            species=self.species,
            location=Point(5, 5)
        )
        
        # Create plant state
        self.state = PlantState.objects.create(name="Test State")
    
    def test_plant_geojson_serializer(self):
        """Test that PlantGeoSerializer produces valid GeoJSON."""
        serializer = PlantGeoSerializer(self.plant, context={'request': None})
        data = serializer.data
        
        # Debug output
        print("Plant GeoJSON data:", data)
        
        # Verify GeoJSON structure
        self.assertEqual(data['type'], 'Feature')
        self.assertIn('geometry', data)
        self.assertIn('properties', data)
        
        # Verify geometry
        self.assertEqual(data['geometry']['type'], 'Point')
        self.assertEqual(len(data['geometry']['coordinates']), 2)
        self.assertEqual(data['geometry']['coordinates'][0], 5.0)
        self.assertEqual(data['geometry']['coordinates'][1], 5.0)
        
        # Verify properties
        self.assertEqual(data['properties']['name'], str(self.species))
    
    def test_zone_geojson_serializer(self):
        """Test that ZoneGeoSerializer produces valid GeoJSON."""
        serializer = ZoneGeoSerializer(self.zone, context={'request': None})
        data = serializer.data
        
        # Debug output
        print("Zone GeoJSON data:", data)
        
        # Verify GeoJSON structure
        self.assertEqual(data['type'], 'Feature')
        self.assertIn('geometry', data)
        self.assertIn('properties', data)
        
        # Verify geometry
        self.assertEqual(data['geometry']['type'], 'MultiPolygon')
        
        # Verify properties
        self.assertEqual(data['properties']['name'], "Test Zone")
        self.assertEqual(data['properties']['kind']['name'], "Test Zone Kind")