from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for all resources
router = DefaultRouter()

# Main resources
router.register(r'plants', views.PlantViewSet)
router.register(r'zones', views.ZoneViewSet)

# Plant-related resources with explicit path prefixes for nesting
router.register(r'plants-states', views.PlantStateViewSet, basename='plantstate')
router.register(r'plants-state-transitions', views.PlantStateTransitionViewSet, basename='plantstatetransition')
router.register(r'plants-images', views.PlantImageViewSet, basename='plantimage')
router.register(r'plants-image-kinds', views.PlantImageKindViewSet, basename='plantimagekind')
router.register(r'plants-logs', views.PlantLogViewSet, basename='plantlog')
router.register(r'plants-log-kinds', views.PlantLogKindViewSet, basename='plantlogkind')

# Zone-related resources with explicit path prefixes for nesting
router.register(r'zones-kinds', views.ZoneKindViewSet, basename='zonekind')

urlpatterns = [
    path('', include(router.urls)),
]