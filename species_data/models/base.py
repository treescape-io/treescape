from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


from species_data.fields import (
    ConfidenceField,
    DecimalEstimatedRange,
    DurationEstimatedRange,
    SourcesField,
)


class CategorizedPlantPropertyManager(models.Manager):
    """Manager for CategorizedPlantPropertyBase."""

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class CategorizedPlantPropertyBase(models.Model):
    """Abstract base model for categorization of species."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True)
    description = models.TextField()

    objects = CategorizedPlantPropertyManager()

    class Meta:
        abstract = True
        ordering = ["name"]

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class PlantPropertiesBase(models.Model):
    """Abstract base class for properties of a species."""

    height = DecimalEstimatedRange(verbose_name=_("mature plant height (m)"))
    width = DecimalEstimatedRange(verbose_name=_("mature plant canopy width (m)"))

    temperature = DecimalEstimatedRange(
        verbose_name=_("temperature tolerance (degrees C)")
    )
    precipitation = DecimalEstimatedRange(
        verbose_name=_("precipitation tolerance (mm/year)")
    )
    soil_acidity = DecimalEstimatedRange(verbose_name=_("soil acidity tolerance (pH)"))
    sun_hours = DurationEstimatedRange(verbose_name=_("sunlight tolerance (h/day)"))

    production_start = DurationEstimatedRange(verbose_name=_("production start"))
    production_peak = DurationEstimatedRange(verbose_name=_("production peak"))
    lifetime = DurationEstimatedRange(verbose_name=_("lifetime"))

    class Meta:
        abstract = True


class CategorizedSpeciesPropertyThroughBase(models.Model):
    """Abstract base model for through of CategorizedPlantPropertyBase <-> SpeciesBase M2M, including confidence and source."""

    sources = SourcesField()  # pyright: ignore[reportCallIssue]
    confidence = ConfidenceField()

    class Meta:
        abstract = True
