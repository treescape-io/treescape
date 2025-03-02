from rest_framework import viewsets
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
from .serializers import (
    PlantSerializer,
    ZoneSerializer,
    ZoneKindSerializer,
    PlantStateSerializer,
    PlantStateTransitionSerializer,
    PlantImageSerializer,
    PlantImageKindSerializer,
    PlantLogSerializer,
    PlantLogKindSerializer
)


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed or edited.
    """
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = 'id'


class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows zones to be viewed or edited.
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    lookup_field = 'id'


class ZoneKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows zone kinds to be viewed or edited.
    """
    queryset = ZoneKind.objects.all()
    serializer_class = ZoneKindSerializer
    lookup_field = 'id'


class PlantStateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant states to be viewed or edited.
    """
    queryset = PlantState.objects.all()
    serializer_class = PlantStateSerializer
    lookup_field = 'id'


class PlantStateTransitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant state transitions to be viewed or edited.
    """
    queryset = PlantStateTransition.objects.all()
    serializer_class = PlantStateTransitionSerializer
    lookup_field = 'id'


class PlantImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant images to be viewed or edited.
    """
    queryset = PlantImage.objects.all()
    serializer_class = PlantImageSerializer
    lookup_field = 'id'


class PlantImageKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant image kinds to be viewed or edited.
    """
    queryset = PlantImageKind.objects.all()
    serializer_class = PlantImageKindSerializer
    lookup_field = 'id'


class PlantLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant logs to be viewed or edited.
    """
    queryset = PlantLog.objects.all()
    serializer_class = PlantLogSerializer
    lookup_field = 'id'


class PlantLogKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant log kinds to be viewed or edited.
    """
    queryset = PlantLogKind.objects.all()
    serializer_class = PlantLogKindSerializer
    lookup_field = 'id'
