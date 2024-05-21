from django.utils.translation import gettext_lazy as _
from django.db import models

from .base import CategorizedPlantPropertyBase, CategorizedSpeciesPropertyThroughBase


class GrowthHabit(CategorizedPlantPropertyBase):
    """Growth habit for plant species (tree, shrub etc.)."""

    class Meta(CategorizedPlantPropertyBase.Meta):
        verbose_name = _("growth habit")
        verbose_name_plural = _("growth habits")


class SpeciesGrowthHabit(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    growth_habit = models.ForeignKey(GrowthHabit, on_delete=models.CASCADE)

    class Meta(CategorizedSpeciesPropertyThroughBase.Meta):
        unique_together = ("species", "growth_habit")


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


class SpeciesClimateZone(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    climate_zone = models.ForeignKey(ClimateZone, on_delete=models.CASCADE)

    class Meta(CategorizedSpeciesPropertyThroughBase.Meta):
        unique_together = ("species", "climate_zone")


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


class SpeciesHumanUse(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    human_use = models.ForeignKey(HumanUse, on_delete=models.CASCADE)

    class Meta(CategorizedSpeciesPropertyThroughBase.Meta):
        unique_together = ("species", "human_use")


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


class SpeciesEcologicalRole(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    ecological_role = models.ForeignKey(EcologicalRole, on_delete=models.CASCADE)

    class Meta(CategorizedSpeciesPropertyThroughBase.Meta):
        unique_together = ("species", "ecological_role")


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


class SpeciesSoilPreference(CategorizedSpeciesPropertyThroughBase):
    species = models.ForeignKey("SpeciesProperties", on_delete=models.CASCADE)
    soil_texture = models.ForeignKey(SoilPreference, on_delete=models.CASCADE)

    class Meta(CategorizedSpeciesPropertyThroughBase.Meta):
        unique_together = ("species", "soil_texture")
