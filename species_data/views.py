from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from plant_species.models import Species, Genus, Family

from .models import (
    ClimateZone,
    GrowthHabit,
    HumanUse,
    EcologicalRole,
    SoilPreference,
    PropagationMethod,
    Source,
)

from .serializers import (
    FamilyDataSerializer,
    GenusDataSerializer,
    SpeciesDataSerializer,
    ClimateZoneSerializer,
    GrowthHabitSerializer,
    HumanUseSerializer,
    EcologicalRoleSerializer,
    SoilPreferenceSerializer,
    PropagationMethodSerializer,
    SourceSerializer,
)


class FamilyDataViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Family.objects.all()
    serializer_class = FamilyDataSerializer


class GenusDataViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Genus.objects.all()
    serializer_class = GenusDataSerializer


class SpeciesDataViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Species.objects.all()
    serializer_class = SpeciesDataSerializer
    filterset_fields = {
        # "properties__genus__family",
        # "properties__genus",
        "properties__temperature_minimum": ["lte"],
        "properties__temperature_maximum": ["gte"],
        "properties__precipitation_minimum": ["lte"],
        "properties__precipitation_maximum": ["gte"],
        "properties__climate_zones": ["exact"],
        "properties__growth_habits": ["exact"],
        "properties__human_uses": ["exact"],
        "properties__ecological_roles": ["exact"],
    }

    search_fields = [
        "latin_name",
        "common_names__name",
        "genus__common_names__name",
        "genus__family__common_names__name",
        "genus__latin_name",
        "genus__family__latin_name",
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class ClimateZoneViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = ClimateZone.objects.all()
    serializer_class = ClimateZoneSerializer


class GrowthHabitViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = GrowthHabit.objects.all()
    serializer_class = GrowthHabitSerializer


class HumanUseViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = HumanUse.objects.all()
    serializer_class = HumanUseSerializer


class EcologicalRoleViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = EcologicalRole.objects.all()
    serializer_class = EcologicalRoleSerializer


class SoilPreferenceViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = SoilPreference.objects.all()
    serializer_class = SoilPreferenceSerializer


class PropagationMethodViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = PropagationMethod.objects.all()
    serializer_class = PropagationMethodSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
