from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from .models import (
    Plant, 
    Zone, 
    ZoneKind, 
    PlantState, 
    PlantStateTransition, 
    PlantImage, 
    PlantImageKind, 
    PlantLog, 
    PlantLogKind
)
from plant_species.models import Species, Genus, SpeciesVariety


class ZoneKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZoneKind
        fields = ['url', 'id', 'name', 'description']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    """Standard serializer for Zone model"""
    
    kind = ZoneKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneKind.objects.all(),
        source='kind',
        write_only=True
    )
    
    class Meta:
        model = Zone
        fields = ['url', 'id', 'name', 'area', 'kind', 'kind_id']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class ZoneGeoSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Zone model"""
    
    kind = ZoneKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneKind.objects.all(),
        source='kind',
        write_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='zone-detail',
        lookup_field='id'
    )
    
    class Meta:
        model = Zone
        geo_field = 'area'
        fields = ['url', 'id', 'name', 'area', 'kind', 'kind_id']
        lookup_field = 'id'


class PlantStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantState
        fields = ['url', 'id', 'name', 'description']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class PlantStateTransitionSerializer(serializers.HyperlinkedModelSerializer):
    from_state = PlantStateSerializer(read_only=True)
    to_state = PlantStateSerializer(read_only=True)
    from_state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(),
        source='from_state',
        write_only=True
    )
    to_state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(),
        source='to_state',
        write_only=True
    )
    
    class Meta:
        model = PlantStateTransition
        fields = ['url', 'id', 'name', 'description', 'from_state', 'to_state', 'from_state_id', 'to_state_id']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class PlantImageKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantImageKind
        fields = ['url', 'id', 'name', 'description']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class PlantImageSerializer(serializers.HyperlinkedModelSerializer):
    kind = PlantImageKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantImageKind.objects.all(),
        source='kind',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = PlantImage
        fields = ['url', 'id', 'plant', 'image', 'kind', 'kind_id', 'timestamp', 'note']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'},
            'plant': {'lookup_field': 'id'}
        }


class PlantLogKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantLogKind
        fields = ['url', 'id', 'name', 'description']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class PlantLogSerializer(serializers.HyperlinkedModelSerializer):
    kind = PlantLogKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantLogKind.objects.all(),
        source='kind',
        write_only=True
    )
    
    class Meta:
        model = PlantLog
        fields = ['url', 'id', 'plant', 'timestamp', 'note', 'kind', 'kind_id']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'},
            'plant': {'lookup_field': 'id'}
        }


class SpeciesSlugRelatedField(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'slug': obj.slug
        }
        return self.reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    """Standard serializer for Plant model"""
    
    # Handle state, which is calculated via get_state method
    state = PlantStateSerializer(source='get_state', read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(),
        write_only=True,
        required=False
    )
    
    # Handle related collections
    images = PlantImageSerializer(many=True, read_only=True)
    logs = PlantLogSerializer(many=True, read_only=True)
    
    # Properly handle species reference
    species_detail = serializers.HyperlinkedRelatedField(
        source='species',
        view_name='species-detail',
        lookup_field='slug',
        read_only=True
    )
    
    # Include custom name field
    name = serializers.CharField(source='get_name', read_only=True)
    
    class Meta:
        model = Plant
        fields = ['url', 'id', 'species', 'species_detail', 'location', 'name', 
                 'genus', 'variety', 'state', 'state_id', 
                 'images', 'logs']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'},
            'species': {'required': False},
            'genus': {'required': False},
            'variety': {'required': False}
        }
    
    def create(self, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop('state_id', None)
        plant = Plant.objects.create(**validated_data)
        
        if state:
            PlantStateTransition.objects.create(plant=plant, state=state)
            
        return plant
        
    def update(self, instance, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop('state_id', None)
        
        # Update instance with all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if state:
            PlantStateTransition.objects.create(plant=instance, state=state)
            
        return instance


class PlantGeoSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Plant model"""
    
    # Handle state, which is calculated via get_state method
    state = PlantStateSerializer(source='get_state', read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(),
        write_only=True,
        required=False
    )
    
    # Handle related collections
    images = PlantImageSerializer(many=True, read_only=True)
    logs = PlantLogSerializer(many=True, read_only=True)
    
    # Properly handle species reference
    species_detail = serializers.HyperlinkedRelatedField(
        source='species',
        view_name='species-detail',
        lookup_field='slug',
        read_only=True
    )
    
    # Include custom name field
    name = serializers.CharField(source='get_name', read_only=True)
    
    # Hyperlinked URL field
    url = serializers.HyperlinkedIdentityField(
        view_name='plant-detail',
        lookup_field='id'
    )
    
    class Meta:
        model = Plant
        geo_field = 'location'
        fields = ['url', 'id', 'species', 'species_detail', 'location', 'name', 
                 'genus', 'variety', 'state', 'state_id', 
                 'images', 'logs']
        lookup_field = 'id'
        extra_kwargs = {
            'species': {'required': False},
            'genus': {'required': False},
            'variety': {'required': False}
        }
    
    def create(self, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop('state_id', None)
        plant = Plant.objects.create(**validated_data)
        
        if state:
            PlantStateTransition.objects.create(plant=plant, state=state)
            
        return plant
        
    def update(self, instance, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop('state_id', None)
        
        # Update instance with all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if state:
            PlantStateTransition.objects.create(plant=instance, state=state)
            
        return instance