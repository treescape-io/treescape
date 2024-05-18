from typing import NamedTuple
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from plant_species.models import Genus, Family, Species, SpeciesVariety
from species_data.fields import DecimalEstimatedRange, DurationEstimatedRange

from .base import PlantPropertiesBase
from .source import SourceType

from .categories import (
    GrowthHabit,
    # FamilyGrowthHabit,
    # GenusGrowthHabit,
    SpeciesGrowthHabit,
    ClimateZone,
    # FamilyClimateZone,
    # GenusClimateZone,
    SpeciesClimateZone,
    HumanUse,
    # FamilyHumanUse,
    # GenusHumanUse,
    SpeciesHumanUse,
    EcologicalRole,
    # FamilyEcologicalRole,
    # GenusEcologicalRole,
    SpeciesEcologicalRole,
    SoilPreference,
    # FamilySoilPreference,
    # GenusSoilPreference,
    SpeciesSoilPreference,
    LightPreference,
    # FamilyLightPreference,
    # GenusLightPreference,
    SpeciesLightPreference,
)


# class FamilyProperties(PlantPropertiesBase):
#     family = models.ForeignKey(Family, on_delete=models.CASCADE)
#     growth_habits = models.ManyToManyField(GrowthHabit, through=FamilyGrowthHabit)
#     climate_zones = models.ManyToManyField(ClimateZone, through=FamilyClimateZone)
#     human_uses = models.ManyToManyField(HumanUse, through=FamilyHumanUse)
#     ecological_roles = models.ManyToManyField(
#         EcologicalRole, through=FamilyEcologicalRole
#     )
#     soil_preference = models.ManyToManyField(
#         SoilPreference, through=FamilySoilPreference
#     )
#     light_preference = models.ManyToManyField(
#         LightPreference, through=FamilyLightPreference
#     )

#     class Meta:
#         verbose_name = _("family properties")
#         verbose_name_plural = _("family properties")


# class GenusProperties(PlantPropertiesBase):
#     genus = models.ForeignKey(Genus, on_delete=models.CASCADE)
#     growth_habits = models.ManyToManyField(GrowthHabit, through=GenusGrowthHabit)
#     climate_zones = models.ManyToManyField(ClimateZone, through=GenusClimateZone)
#     human_uses = models.ManyToManyField(HumanUse, through=GenusHumanUse)
#     ecological_roles = models.ManyToManyField(
#         EcologicalRole, through=GenusEcologicalRole
#     )
#     soil_preference = models.ManyToManyField(
#         SoilPreference, through=GenusSoilPreference
#     )
#     light_preference = models.ManyToManyField(
#         LightPreference, through=GenusLightPreference
#     )

#     class Meta:
#         verbose_name = _("genus properties")
#         verbose_name_plural = _("genus properties")

# TODO: Memoized classmethod on SpeciesProperties


class EnrichmentSource(NamedTuple):
    content: str
    source_type: SourceType


class SpeciesProperties(PlantPropertiesBase):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    growth_habits = models.ManyToManyField(GrowthHabit, through=SpeciesGrowthHabit)
    climate_zones = models.ManyToManyField(ClimateZone, through=SpeciesClimateZone)
    human_uses = models.ManyToManyField(HumanUse, through=SpeciesHumanUse)
    ecological_roles = models.ManyToManyField(
        EcologicalRole, through=SpeciesEcologicalRole
    )
    soil_preference = models.ManyToManyField(
        SoilPreference, through=SpeciesSoilPreference
    )
    light_preference = models.ManyToManyField(
        LightPreference, through=SpeciesLightPreference
    )

    class Meta:
        verbose_name = _("species properties")
        verbose_name_plural = _("species properties")
