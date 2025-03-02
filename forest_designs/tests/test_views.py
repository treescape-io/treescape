import json
from django.test import TestCase
from django.urls import reverse

from forest_designs.models import (
    Plant, PlantState, PlantStateTransition, Zone, ZoneKind
)
from plant_species.tests.test_models import SpeciesTestMixin


class ForestDesignsViewTestMixin(SpeciesTestMixin):
    """Mixin for forest designs view tests."""
    
    def setUp(self):
        """Set up an admin user for authentication."""
        super().setUp()
        from django.contrib.auth.models import User
        
        # Create a superuser for authentication
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        
        # Login the client
        self.client.force_login(self.admin_user)
    
    @classmethod
    def setUpTestData(cls):
        # Call parent setUpTestData to create species data
        super().setUpTestData()
        
        # Create states using get_or_create to avoid uniqueness conflicts
        cls.state1, _ = PlantState.objects.get_or_create(name="Planned")
        cls.state2, _ = PlantState.objects.get_or_create(name="Planted")
        
        # Create zone and zone kind - use unique names with a random suffix for tests
        import uuid
        unique_suffix = str(uuid.uuid4())[:8]
        
        cls.zone_kind, _ = ZoneKind.objects.get_or_create(
            name=f"Test Zone Kind {unique_suffix}"
        )
        cls.zone, _ = Zone.objects.get_or_create(
            name=f"Test Zone {unique_suffix}",
            kind=cls.zone_kind,
            defaults={"area": "MULTIPOLYGON(((0 0, 0 10, 10 10, 10 0, 0 0)))"}
        )


class PlantViewTestCase(ForestDesignsViewTestMixin, TestCase):
    """Test the Plant API views."""
    
    def setUp(self):
        """Set up test client and create a plant for testing."""
        super().setUp()
        
        # Create a plant with a unique location
        import random
        x, y = random.uniform(1, 9), random.uniform(1, 9)
        
        # Create a plant
        self.plant = Plant.objects.create(
            species=self.species,
            location=f"POINT({x} {y})"
        )
        
        # Create an initial state transition
        self.transition = PlantStateTransition.objects.create(
            plant=self.plant,
            state=self.state1
        )
    
    def test_plant_list(self):
        """Test that plant list endpoint works correctly."""
        response = self.client.get(reverse('plant-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)
    
    def test_plant_detail(self):
        """Test that plant detail endpoint works correctly."""
        response = self.client.get(reverse('plant-detail', kwargs={'id': self.plant.id}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], str(self.species))
    
    def test_plant_state_serialization(self):
        """Test that plant state is correctly serialized."""
        response = self.client.get(reverse('plant-detail', kwargs={'id': self.plant.id}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['state']['name'], "Planned")
    
    def test_plant_state_update(self):
        """Test updating a plant's state."""
        url = reverse('plant-detail', kwargs={'id': self.plant.id})
        data = {'state_id': self.state2.id}
        response = self.client.patch(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that a new transition was created
        self.assertEqual(PlantStateTransition.objects.filter(plant=self.plant).count(), 2)
        
        # Check that the state is updated in the response
        latest_response = self.client.get(url)
        data = json.loads(latest_response.content)
        self.assertEqual(data['state']['name'], "Planted")
    
    def test_create_plant_with_state(self):
        """Test creating a new plant with an initial state."""
        url = reverse('plant-list')
        
        # Use random coordinates for unique location
        import random
        x, y = random.uniform(10, 20), random.uniform(10, 20)
        
        # Use the UUID directly instead of URL
        data = {
            'species': str(self.species.uuid),  # Use the UUID as a string
            'location': f'POINT({x} {y})',  # Use WKT format for the point
            'state_id': self.state2.id
        }
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        
        # If response is not 201, print the error message to help debug
        if response.status_code != 201:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            
        self.assertEqual(response.status_code, 201)
        
        # Check that the plant was created
        data = json.loads(response.content)
        plant_id = data['id']
        plant = Plant.objects.get(id=plant_id)
        
        # Check that a state transition was created
        transition = PlantStateTransition.objects.filter(plant=plant).first()
        self.assertEqual(transition.state, self.state2)


class ZoneViewTestCase(ForestDesignsViewTestMixin, TestCase):
    """Test the Zone API views."""
    
    def test_zone_list(self):
        """Test that zone list endpoint works correctly."""
        response = self.client.get(reverse('zone-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)
        # Use the zone created in setUpTestData instead of hardcoded name
        self.assertEqual(data['results'][0]['name'], self.zone.name)
    
    def test_zone_detail(self):
        """Test that zone detail endpoint works correctly."""
        response = self.client.get(reverse('zone-detail', kwargs={'id': self.zone.id}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], self.zone.name)
        self.assertEqual(data['kind']['name'], self.zone_kind.name)
    
    def test_create_zone(self):
        """Test creating a new zone."""
        url = reverse('zone-list')
        
        # Use a unique name for the zone
        import uuid
        unique_name = f"New Test Zone {uuid.uuid4()}"
        
        # Use a slightly different geometry
        import random
        offset = random.uniform(20, 30)
        
        data = {
            'name': unique_name,
            'kind_id': self.zone_kind.id,
            'area': json.dumps({
                'type': 'MultiPolygon',
                'coordinates': [[[[offset, offset], [offset, offset+5], [offset+5, offset+5], [offset+5, offset], [offset, offset]]]]
            })
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check that the zone was created
        data = json.loads(response.content)
        zone_id = data['id']
        zone = Zone.objects.get(id=zone_id)
        self.assertEqual(zone.name, unique_name)
        self.assertEqual(zone.kind, self.zone_kind)


class PlantStateViewTestCase(ForestDesignsViewTestMixin, TestCase):
    """Test the PlantState API views."""
    
    def test_plant_state_list(self):
        """Test that plant state list endpoint works correctly."""
        url = reverse('plantstate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verify our states exist in results, don't check exact count
        state_names = [state['name'] for state in data['results']]
        self.assertIn("Planned", state_names)
        self.assertIn("Planted", state_names)
    
    def test_create_plant_state(self):
        """Test creating a new plant state."""
        import uuid
        unique_name = f"Removed-{uuid.uuid4()}"
        
        url = reverse('plantstate-list')
        data = {
            'name': unique_name,
            'description': 'Plant has been removed or died'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check that the state was created
        data = json.loads(response.content)
        state_id = data['id']
        state = PlantState.objects.get(id=state_id)
        self.assertEqual(state.name, unique_name)
        self.assertEqual(state.description, "Plant has been removed or died")