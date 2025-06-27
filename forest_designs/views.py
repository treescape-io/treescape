from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter, TMSTileFilter
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
from .serializers import (
    PlantSerializer,
    PlantGeoSerializer,
    ZoneSerializer,
    ZoneGeoSerializer,
    ZoneKindSerializer,
    PlantStateSerializer,
    PlantStateTransitionSerializer,
    PlantImageSerializer,
    PlantImageKindSerializer,
    PlantLogSerializer,
    PlantLogKindSerializer,
)


class GeoJSONNegotiationMixin:
    """Mixin that adds content negotiation for GeoJSON format"""

    def get_serializer_class(self):
        if self.request and self.request.query_params.get("format") == "geojson":
            return self.geojson_serializer_class
        return super().get_serializer_class()


class PlantViewSet(GeoJSONNegotiationMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows plants to be viewed or edited.

    Supports both standard JSON and GeoJSON formats.
    Get GeoJSON with ?format=geojson

    Spatial filtering:
    - ?in_bbox=min_lon,min_lat,max_lon,max_lat (SW lon, SW lat, NE lon, NE lat)
    - ?tile=zoom,x,y (TMS tile coordinates)
    """

    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    geojson_serializer_class = PlantGeoSerializer
    lookup_field = "id"

    # Add spatial filters
    bbox_filter_field = "location"
    bbox_filter_include_overlapping = (
        True  # Include plants with location overlapping the bbox
    )
    tile_filter_field = "location"
    filter_backends = (DjangoFilterBackend, InBBoxFilter, TMSTileFilter)


class ZoneViewSet(GeoJSONNegotiationMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows zones to be viewed or edited.

    Supports both standard JSON and GeoJSON formats.
    Get GeoJSON with ?format=geojson

    Spatial filtering:
    - ?in_bbox=min_lon,min_lat,max_lon,max_lat (SW lon, SW lat, NE lon, NE lat)
    - ?tile=zoom,x,y (TMS tile coordinates)
    """

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    geojson_serializer_class = ZoneGeoSerializer
    lookup_field = "id"

    # Add spatial filters
    bbox_filter_field = "area"
    bbox_filter_include_overlapping = (
        True  # Include zones with area overlapping the bbox
    )
    tile_filter_field = "area"
    filter_backends = (DjangoFilterBackend, InBBoxFilter, TMSTileFilter)


class ZoneKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows zone kinds to be viewed or edited.
    """

    queryset = ZoneKind.objects.all()
    serializer_class = ZoneKindSerializer
    lookup_field = "id"


class PlantStateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant states to be viewed or edited.
    """

    queryset = PlantState.objects.all()
    serializer_class = PlantStateSerializer
    lookup_field = "id"


class PlantStateTransitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant state transitions to be viewed or edited.
    """

    queryset = PlantStateTransition.objects.all()
    serializer_class = PlantStateTransitionSerializer
    lookup_field = "id"


class PlantImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant images to be viewed or edited.
    """

    queryset = PlantImage.objects.all()
    serializer_class = PlantImageSerializer
    lookup_field = "id"


class PlantImageKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant image kinds to be viewed or edited.
    """

    queryset = PlantImageKind.objects.all()
    serializer_class = PlantImageKindSerializer
    lookup_field = "id"


class PlantLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant logs to be viewed or edited.
    """

    queryset = PlantLog.objects.all()
    serializer_class = PlantLogSerializer
    lookup_field = "id"


class PlantLogKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plant log kinds to be viewed or edited.
    """

    queryset = PlantLogKind.objects.all()
    serializer_class = PlantLogKindSerializer
    lookup_field = "id"
