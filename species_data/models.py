from django.utils.translation import gettext_lazy as _
from django.db import models


class SpeciesDataBase(models.Model):
    """Abstract base model for species data."""

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True
        ordering = ["name"]


class GrowthHabit(SpeciesDataBase):
    """Growth habit for plant species."""

    class Meta(SpeciesDataBase.Meta):
        verbose_name = _("growth habit")
        verbose_name_plural = _("growth habits")


class ClimateZone(SpeciesDataBase):
    """Köppen-Geiger climate zones."""

    code = models.CharField(_("code"), max_length=3)

    class Meta(SpeciesDataBase.Meta):
        verbose_name = _("climate zone")
        verbose_name_plural = _("climate zones")
        ordering = ["code"]


class HumanUse(SpeciesDataBase):
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

    class Meta(SpeciesDataBase.Meta):
        verbose_name = _("human use")
        verbose_name_plural = _("human uses")


class EcologicalRole(SpeciesDataBase):
    """Various ecological roles."""

    class Meta(SpeciesDataBase.Meta):
        verbose_name = _("ecological role")
        verbose_name_plural = _("ecological roles")
