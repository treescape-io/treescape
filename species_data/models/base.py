from django.db import models
from django.utils.translation import gettext_lazy as _

from .source import Source

from species_data.fields import (
    ConfidenceField,
    DecimalEstimatedRange,
    DurationEstimatedRange,
)


class CategorizedPlantPropertyBase(models.Model):
    """Abstract base model for categorization of species."""

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True
        ordering = ["name"]


class PlantPropertiesBase(models.Model):
    """Abstract base class for properties of a species."""

    height = DecimalEstimatedRange(verbose_name=_("plant height (m)"))
    width = DecimalEstimatedRange(verbose_name=_("canopy width (m)"))

    soil_acidity = DecimalEstimatedRange(verbose_name=_("preferred soil acidity (pH)"))

    production_start = DurationEstimatedRange(verbose_name=_("production start"))
    production_peak = DurationEstimatedRange(verbose_name=_("production peak"))
    lifetime = DurationEstimatedRange(verbose_name=_("lifetime"))

    class Meta:
        abstract = True


class CategorizedSpeciesPropertyThroughBase(models.Model):
    """Abstract base model for through of CategorizedPlantPropertyBase <-> SpeciesBase M2M, including confidence and source."""

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    confidence = ConfidenceField()

    class Meta:
        abstract = True
