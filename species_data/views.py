from rest_framework import viewsets

from plant_species.models import Species, Genus, Family

from .models import (
    ClimateZone,
    GrowthHabit,
    HumanUse,
    EcologicalRole,
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


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
