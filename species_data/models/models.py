from django.db import models
from django.utils.translation import gettext_lazy as _

from plant_species.models import Species

from .base import PlantPropertiesBase

from .categories import (
    GrowthHabit,
    PropagationMethod,
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
    SpeciesPropagationMethod,
    # FamilySoilPreference,
    # GenusSoilPreference,
    SpeciesSoilPreference,
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


# Natural key lookups by species.slug
class SpeciesPropertiesManager(models.Manager):
    def get_by_natural_key(self, species_slug):
        return self.get(species__slug=species_slug)


class SpeciesProperties(PlantPropertiesBase):
    species = models.OneToOneField(
        Species,
        on_delete=models.CASCADE,
        related_name="properties",
        db_column="species_uuid",
    )
    growth_habits = models.ManyToManyField(GrowthHabit, through=SpeciesGrowthHabit)
    climate_zones = models.ManyToManyField(ClimateZone, through=SpeciesClimateZone)
    human_uses = models.ManyToManyField(HumanUse, through=SpeciesHumanUse)
    ecological_roles = models.ManyToManyField(
        EcologicalRole, through=SpeciesEcologicalRole
    )
    soil_preferences = models.ManyToManyField(
        SoilPreference, through=SpeciesSoilPreference
    )
    propagation_methods = models.ManyToManyField(
        PropagationMethod, through=SpeciesPropagationMethod
    )

    objects = SpeciesPropertiesManager()

    def natural_key(self):
        return (self.species.slug,)

    class Meta:
        verbose_name = _("species properties")
        verbose_name_plural = _("species properties")

    def __str__(self):
        if self.species:
            return str(self.species)

        return super().__str__()
