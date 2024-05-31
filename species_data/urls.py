from rest_framework import routers
from species_data import views

router = routers.DefaultRouter()
router.register(r"families", views.FamilyDataViewSet)
router.register(r"genera", views.GenusDataViewSet)
router.register(r"species", views.SpeciesDataViewSet)
router.register(r"climatezones", views.ClimateZoneViewSet)
router.register(r"growthhabits", views.GrowthHabitViewSet)
router.register(r"humanuses", views.HumanUseViewSet)
router.register(r"ecologicalroles", views.EcologicalRoleViewSet)
router.register(r"soilpreference", views.SoilPreferenceViewSet)
router.register(r"propagationmethod", views.PropagationMethodViewSet)
router.register(r"sources", views.SourceViewSet)

app_name = "species_data"

urlpatterns = router.urls
