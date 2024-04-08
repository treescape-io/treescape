from django.utils.translation import gettext_lazy as _
from django.db import models

from .base import CategorizedPlantPropertyBase, CategorizedSpeciesPropertyThroughBase


class GrowthHabit(CategorizedPlantPropertyBase):
    """Growth habit for plant species (tree, shrub etc.)."""

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("growth habit")
        verbose_name_plural = _("growth habits")


class GrowthHabitThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(GrowthHabit.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None


# class FamilyGrowthHabit(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     growth_habit = models.ForeignKey(GrowthHabit, on_delete=models.CASCADE)


# class GenusGrowthHabit(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     growth_habit = models.ForeignKey(GrowthHabit, on_delete=models.CASCADE)


class SpeciesGrowthHabit(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    growth_habit = models.ForeignKey(GrowthHabit, on_delete=models.CASCADE)


class ClimateZone(CategorizedPlantPropertyBase):
    """Köppen-Geiger climate zones (Tropical Rainforest, Temperate, No Dry Season, Cold Summer etc.)."""

    class MainGroup(models.TextChoices):
        A = "A", _("A: Tropical")
        B = "B", _("B: Dry")
        C = "C", _("C: Temperate")
        D = "D", _("D: Continental")
        E = "E", _("E: Polar")

    main_group = models.CharField(
        _("main group"),
        max_length=1,
        choices=MainGroup.choices,
    )

    class SeasonalPrecipitation(models.TextChoices):
        S = "S", _("S: Semi-Arid or steppe")
        W = "W", _("W: Arid Desert")
        f = "f", _("f: No dry season")
        m = "m", _("m: Monsoon")
        w = "w", _("w: Wet winter")
        s = "s", _("s: Wet summer")

    seasonal_precipitation = models.CharField(
        _("seasonal precipitation"),
        max_length=1,
        choices=SeasonalPrecipitation.choices,
        null=True,
        blank=True,
    )

    class HeatLevel(models.TextChoices):
        h = "h", _("h: Hot arid")
        k = "k", _("k: Cold arid")
        a = "a", _("a: Hot summer")
        b = "b", _("b: Warm summer")
        c = "c", _("c: Cool summer")
        d = "d", _("d: Very cold winter")
        T = "T", _("T: Tundra")
        F = "F", _("F: Ice cap")

    heat_level = models.CharField(
        _("heat level"),
        max_length=1,
        choices=HeatLevel.choices,
        null=True,
        blank=True,
    )

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("climate zone")
        verbose_name_plural = _("climate zones")
        ordering = ("main_group", "seasonal_precipitation", "heat_level")
        unique_together = ("main_group", "seasonal_precipitation", "heat_level")

    def __str__(self):
        return f"{self.main_group}{self.seasonal_precipitation or ''}{self.heat_level or ''}: {self.name}"


class ClimateZoneThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(ClimateZone.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None


# class FamilyClimateZone(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     climate_zone = models.ForeignKey(ClimateZone, on_delete=models.CASCADE)


# class GenusClimateZone(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     climate_zone = models.ForeignKey(ClimateZone, on_delete=models.CASCADE)


class SpeciesClimateZone(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    climate_zone = models.ForeignKey(ClimateZone, on_delete=models.CASCADE)


class HumanUse(CategorizedPlantPropertyBase):
    """Various kinds of human uses."""

    class UseType(models.TextChoices):
        FOOD = "food", _("Food")
        MEDICINAL = "medicinal", _("Medicinal")
        MATERIAL = "material", _("Material")
        ORNAMENTAL = "ornamental", _("Ornamental")
        OTHER = "other", _("Other")

    use_type = models.CharField(
        _("use type"),
        max_length=16,
        choices=UseType.choices,
        db_index=True,
    )

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("human use")
        verbose_name_plural = _("human uses")
        ordering = ("use_type", "name")


# class FamilyHumanUse(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     human_use = models.ForeignKey(HumanUse, on_delete=models.CASCADE)


# class GenusHumanUse(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     human_use = models.ForeignKey(HumanUse, on_delete=models.CASCADE)


class SpeciesHumanUse(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    human_use = models.ForeignKey(HumanUse, on_delete=models.CASCADE)


class HumanUseThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(HumanUse.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None

    description = models.TextField(
        _("description"), help_text=_("Description of specific human use.")
    )


class EcologicalRole(CategorizedPlantPropertyBase):
    """Various ecological roles."""

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("ecological role")
        verbose_name_plural = _("ecological roles")


class EcologicalRoleThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(EcologicalRole.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None

    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Optional description of specific ecological role."),
    )


# class FamilyEcologicalRole(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     ecological_role = models.ForeignKey(EcologicalRole, on_delete=models.CASCADE)


# class GenusEcologicalRole(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     ecological_role = models.ForeignKey(EcologicalRole, on_delete=models.CASCADE)


class SpeciesEcologicalRole(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    ecological_role = models.ForeignKey(EcologicalRole, on_delete=models.CASCADE)


class SoilPreference(CategorizedPlantPropertyBase):
    """Soil texture, e.g. loamy, sandy, clayey etc."""

    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
        help_text=_("Optional description of soil preference."),
    )

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("soil texture")
        verbose_name_plural = _("soil textures")


class SoilPreferenceThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(SoilPreference.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None


# class FamilySoilPreference(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     soil_texture = models.ForeignKey(SoilPreference, on_delete=models.CASCADE)


# class GenusSoilPreference(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     soil_texture = models.ForeignKey(SoilPreference, on_delete=models.CASCADE)


class SpeciesSoilPreference(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    soil_texture = models.ForeignKey(SoilPreference, on_delete=models.CASCADE)


class LightPreference(CategorizedPlantPropertyBase):
    """Light preference, e.g. full sun, partial shade, full shade etc."""

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("light preference")
        verbose_name_plural = _("light preferences")


class LightPreferenceThroughBase(CategorizedSpeciesPropertyThroughBase):
    class Meta(LightPreference.Meta, CategorizedSpeciesPropertyThroughBase.Meta):
        ordering = None


# class FamilyLightPreference(CategorizedSpeciesPropertyThroughBase):
#     family = models.ForeignKey("FamilyProperties", on_delete=models.CASCADE)
#     light_preference = models.ForeignKey(LightPreference, on_delete=models.CASCADE)


# class GenusLightPreference(CategorizedSpeciesPropertyThroughBase):
#     genus = models.ForeignKey("GenusProperties", on_delete=models.CASCADE)
#     light_preference = models.ForeignKey(LightPreference, on_delete=models.CASCADE)


class SpeciesLightPreference(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    light_preference = models.ForeignKey(LightPreference, on_delete=models.CASCADE)
