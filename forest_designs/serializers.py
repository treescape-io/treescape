from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (
    Plant,
    Zone,
    ZoneKind,
    PlantState,
    PlantStateTransition,
    PlantImage,
    PlantImageKind,
    PlantLog,
    PlantLogKind,
)


class ZoneKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZoneKind
        fields = ["url", "id", "name", "description"]
        extra_kwargs = {"url": {"lookup_field": "id"}}


class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    """Standard serializer for Zone model"""

    kind = ZoneKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneKind.objects.all(), source="kind", write_only=True
    )

    class Meta:
        model = Zone
        fields = ["url", "id", "name", "area", "kind", "kind_id"]
        extra_kwargs = {"url": {"lookup_field": "id"}}


class ZoneGeoSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for Zone model"""

    kind = ZoneKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneKind.objects.all(), source="kind", write_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="zone-detail", lookup_field="id"
    )

    class Meta:
        model = Zone
        geo_field = "area"
        fields = ["url", "id", "name", "area", "kind", "kind_id"]


class PlantStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantState
        fields = ["url", "id", "name", "description"]
        extra_kwargs = {"url": {"lookup_field": "id"}}


class PlantStateTransitionSerializer(serializers.HyperlinkedModelSerializer):
    state = PlantStateSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(),
        source='state',
        write_only=True
    )
    
    url = serializers.HyperlinkedIdentityField(
        view_name='plantstatetransition-detail',
        lookup_field='id'
    )
    
    plant = serializers.HyperlinkedRelatedField(
        view_name='plant-detail',
        lookup_field='id',
        queryset=Plant.objects.all()
    )
    
    class Meta:
        model = PlantStateTransition
        fields = ['url', 'id', 'plant', 'date', 'state', 'state_id']


class PlantImageKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantImageKind
        fields = ["url", "id", "name", "description"]
        extra_kwargs = {"url": {"lookup_field": "id"}}


class PlantImageSerializer(serializers.HyperlinkedModelSerializer):
    kind = PlantImageKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantImageKind.objects.all(),
        source="kind",
        write_only=True,
        required=False,
    )

    url = serializers.HyperlinkedIdentityField(
        view_name="plantimage-detail", lookup_field="id"
    )

    plant = serializers.HyperlinkedRelatedField(
        view_name="plant-detail", lookup_field="id", queryset=Plant.objects.all()
    )

    class Meta:
        model = PlantImage
        fields = ["url", "id", "plant", "image", "kind", "kind_id", "date"]


class PlantLogKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantLogKind
        fields = ["url", "id", "name", "description"]
        extra_kwargs = {"url": {"lookup_field": "id"}}


class PlantLogSerializer(serializers.HyperlinkedModelSerializer):
    kind = PlantLogKindSerializer(read_only=True)
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantLogKind.objects.all(), source="kind", write_only=True
    )

    url = serializers.HyperlinkedIdentityField(
        view_name="plantlog-detail", lookup_field="id"
    )

    plant = serializers.HyperlinkedRelatedField(
        view_name="plant-detail", lookup_field="id", queryset=Plant.objects.all()
    )

    class Meta:
        model = PlantLog
        fields = ["url", "id", "plant", "date", "notes", "kind", "kind_id"]


class SpeciesSlugRelatedField(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {"slug": obj.slug}
        return self.reverse(
            view_name, kwargs=url_kwargs, request=request, format=format
        )

    def get_attribute(self, instance):
        if instance is None:
            return None

        try:
            return super().get_attribute(instance)
        except (KeyError, AttributeError):
            return None


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    """Standard serializer for Plant model"""

    # Handle state, which is calculated via get_state method
    state = PlantStateSerializer(source="get_state", read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(), write_only=True, required=False
    )

    # Handle related collections
    images = PlantImageSerializer(many=True, read_only=True)
    logs = PlantLogSerializer(many=True, read_only=True)

    # Properly handle species reference
    species_detail = serializers.HyperlinkedRelatedField(
        source="species",
        view_name="species-detail",
        lookup_field="slug",
        read_only=True,
    )

    # Include custom name field
    name = serializers.CharField(source="get_name", read_only=True)

    class Meta:
        model = Plant
        fields = [
            "url",
            "id",
            "species",
            "species_detail",
            "location",
            "name",
            "genus",
            "variety",
            "state",
            "state_id",
            "images",
            "logs",
        ]
        extra_kwargs = {
            "url": {"lookup_field": "id"},
            "species": {"required": False},
            "genus": {"required": False},
            "variety": {"required": False},
        }

    def create(self, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop("state_id", None)
        plant = Plant.objects.create(**validated_data)

        if state:
            PlantStateTransition.objects.create(plant=plant, state=state)

        return plant

    def update(self, instance, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop("state_id", None)

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
    state = PlantStateSerializer(source="get_state", read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantState.objects.all(), write_only=True, required=False
    )

    # Handle related collections
    images = PlantImageSerializer(many=True, read_only=True)
    logs = PlantLogSerializer(many=True, read_only=True)

    # Properly handle species reference
    species_detail = serializers.HyperlinkedRelatedField(
        source="species",
        view_name="species-detail",
        lookup_field="slug",
        read_only=True,
    )

    # Include custom name field
    name = serializers.CharField(source="get_name", read_only=True)

    # Hyperlinked URL field
    url = serializers.HyperlinkedIdentityField(
        view_name="plant-detail", lookup_field="id"
    )

    class Meta:
        model = Plant
        geo_field = "location"
        fields = [
            "url",
            "id",
            "species",
            "species_detail",
            "location",
            "name",
            "genus",
            "variety",
            "state",
            "state_id",
            "images",
            "logs",
        ]
        extra_kwargs = {
            "species": {"required": False},
            "genus": {"required": False},
            "variety": {"required": False},
        }

    def create(self, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop("state_id", None)
        plant = Plant.objects.create(**validated_data)

        if state:
            PlantStateTransition.objects.create(plant=plant, state=state)

        return plant

    def update(self, instance, validated_data):
        # Handle state transition creation if state_id is provided
        state = validated_data.pop("state_id", None)

        # Update instance with all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if state:
            PlantStateTransition.objects.create(plant=instance, state=state)

        return instance
