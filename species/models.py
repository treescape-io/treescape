from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Family(models.Model):
    """Represents a biological family, which is a higher classification group that contains one or more genera."""

    latin_name = models.CharField(_("latin name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the Latin name of the family."""
        return self.latin_name

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")
        ordering = ["latin_name"]


class Genus(models.Model):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")
    latin_name = models.CharField(_("latin name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the name of the genus."""
        return self.latin_name

    class Meta:
        verbose_name = _("genus")
        verbose_name_plural = _("genera")
        ordering = ["latin_name"]


class Species(models.Model):
    """Represents a biological species with a Latin name."""

    genus = models.ForeignKey(Genus, on_delete=models.PROTECT, related_name="species")
    latin_name = models.CharField(_("latin name"), max_length=255)

    def __str__(self):
        """Returns the Latin name of the species."""
        return self.latin_name

    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")
        ordering = ["latin_name"]


class SpeciesCommonName(models.Model):
    """Represents a common name for a species in a specific language."""

    language = models.CharField(
        max_length=7, choices=settings.LANGUAGES, verbose_name=_("Language")
    )
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    name = models.CharField(_("common name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the common name and its language."""
        return self.name

    class Meta:
        verbose_name = _("common name")
        verbose_name_plural = _("common names")
        ordering = ["language", "name"]
        unique_together = (
            "language",
            "species",
            "name",
        )  # Assuming a species cannot have the same common name in the same language


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
