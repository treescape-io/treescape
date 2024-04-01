from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SpeciesBase(models.Model):
    """Abstract base class for species models."""

    latin_name = models.CharField(_("latin name"), max_length=255, unique=True)

    def __str__(self):
        """Returns the Latin name of the family."""
        return self.latin_name

    class Meta:
        abstract = True
        ordering = ["latin_name"]


class Family(SpeciesBase):
    """Represents a biological family, which is a higher classification group that contains one or more genera."""

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")


class Genus(SpeciesBase):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")

    class Meta:
        verbose_name = _("genus")
        verbose_name_plural = _("genera")


class Species(SpeciesBase):
    """Represents a biological species with a Latin name."""

    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")


class CommonNameBase(models.Model):
    """Abstract base class for common names."""

    language = models.CharField(_("language"), max_length=7, choices=settings.LANGUAGES)
    name = models.CharField(_("common name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the common name and its language."""
        return self.name

    class Meta:
        verbose_name = _("common name")
        verbose_name_plural = _("common names")
        ordering = ["language", "name"]
        abstract = True


class FamilyCommonName(CommonNameBase):
    """Represents a common name for a family in a specific language."""

    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "family",
            "language",
            "name",
        )


class GenusCommonName(CommonNameBase):
    """Represents a common name for a genus in a specific language."""

    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "genus",
            "language",
            "name",
        )


class SpeciesCommonName(CommonNameBase):
    """Represents a common name for a species in a specific language."""

    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "species",
            "language",
            "name",
        )


class Variety(models.Model):
    """Represents a variety of a species."""

    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="varieties"
    )
    name = models.CharField(_("variety name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the name of the variety and its species."""
        return f"{self.name} - {self.species.latin_name}"

    class Meta:
        verbose_name = _("variety")
        verbose_name_plural = _("varieties")
        ordering = ["species__latin_name", "name"]
        unique_together = (
            "species",
            "name",
        )  # Assuming a species cannot have two varieties with the same name
