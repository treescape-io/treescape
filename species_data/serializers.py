from rest_framework import serializers

from plant_species.models import Species, Genus, Family
from species_data.models.source import SourceType

from .models import (
    SpeciesProperties,
    ClimateZone,
    GrowthHabit,
    HumanUse,
    EcologicalRole,
    SoilPreference,
    PropagationMethod,
    Source,
)


class FamilyDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Family
        fields = [
            "url",
            "slug",
            "latin_name",
            "description",
            "gbif_id",
            "image_thumbnail",
            "image_large",
        ]
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenusDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genus
        fields = [
            "url",
            "slug",
            "latin_name",
            "description",
            "gbif_id",
            "image_thumbnail",
            "image_large",
        ]
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class SourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceType
        fields = "__all__"


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"

    source_type = SourceTypeSerializer(read_only=True)


class ClimateZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClimateZone
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}

    # TODO: Add source


class GrowthHabitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GrowthHabit
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class HumanUseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumanUse
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class EcologicalRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EcologicalRole
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class SoilPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilPreference
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class PropagationMethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PropagationMethod
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class SpeciesPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesProperties
        fields = [
            "height_maximum",
            "height_confidence",
            "height_maximum",
            "height_source",
            "width_minimum",
            "width_typical",
            "width_maximum",
            "width_confidence",
            "width_source",
            "soil_acidity_minimum",
            "soil_acidity_typical",
            "soil_acidity_maximum",
            "soil_acidity_confidence",
            "soil_acidity_source",
            "climate_zones",
            "growth_habits",
            "human_uses",
            "ecological_roles",
            "soil_preferences",
            "propagation_methods",
        ]

    height_source = serializers.HyperlinkedRelatedField(
        view_name="source-detail", read_only=True
    )
    width_source = serializers.HyperlinkedRelatedField(
        view_name="source-detail", read_only=True
    )
    soil_acidity_source = serializers.HyperlinkedRelatedField(
        view_name="source-detail", read_only=True
    )

    climate_zones = serializers.HyperlinkedRelatedField(
        many=True, view_name="climatezone-detail", read_only=True, lookup_field="slug"
    )
    growth_habits = serializers.HyperlinkedRelatedField(
        many=True, view_name="growthhabit-detail", read_only=True, lookup_field="slug"
    )
    human_uses = serializers.HyperlinkedRelatedField(
        many=True, view_name="humanuse-detail", read_only=True, lookup_field="slug"
    )
    ecological_roles = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="ecologicalrole-detail",
        read_only=True,
        lookup_field="slug",
    )
    soil_preferences = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="soilpreference-detail",
        read_only=True,
        lookup_field="slug",
    )
    propagation_methods = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="propagationmethod-detail",
        read_only=True,
        lookup_field="slug",
    )


class SpeciesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = [
            "url",
            "slug",
            "latin_name",
            "description",
            "gbif_id",
            "image_thumbnail",
            "image_large",
            "properties",
        ]
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}

    properties = SpeciesPropertiesSerializer(read_only=True)
