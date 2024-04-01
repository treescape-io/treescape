from prettyprinter import cpprint, set_default_style
from pygbif import species

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


set_default_style("light")


class SpeciesBase(models.Model):
    """Abstract base class for species models."""

    latin_name = models.CharField(_("latin name"), max_length=255, unique=True)
    gbif_id = models.IntegerField(
        _("GBIF usageKey"), null=True, blank=True, unique=True
    )

    def __str__(self):
        """Returns the Latin name of the family."""
        return self.latin_name

    def _enrich_by_name(self, rank):
        """Fetch species data from GBIF backbone based on the latin name and updates the instance."""

        assert self.latin_name, "Species name required to enrich data."
        assert self.latin_name, "Species name required to call enrich_species_data()."
        assert rank in ["FAMILY", "GENUS", "SPECIES"]

        # Calls https://techdocs.gbif.org/en/openapi/v1/species#/Searching%20names/matchNames
        species_data = species.name_backbone(
            name=self.latin_name,
            rank=rank,
            kingdom="plants",
            limit=2,  # We're basically resolving here - don't need a list!,
            strict=False,  # Never match a taxon in the upper classification
        )

        """ Returns something like this:
        {'canonicalName': 'Quercus robur',
         'class': 'Magnoliopsida',
         'classKey': 220,
         'confidence': 98,
         'family': 'Fagaceae',
         'familyKey': 4689,
         'genus': 'Quercus',
         'genusKey': 2877951,
         'kingdom': 'Plantae',
         'kingdomKey': 6,
         'matchType': 'EXACT',
         'order': 'Fagales',
         'orderKey': 1354,
         'phylum': 'Tracheophyta',
         'phylumKey': 7707728,
         'rank': 'SPECIES',
         'scientificName': 'Quercus robur L.',
         'species': 'Quercus robur',
         'speciesKey': 2878688,
         'status': 'ACCEPTED',
         'synonym': False,
         'usageKey': 2878688}
         """

        if species_data["matchType"] == "NONE":
            raise Exception("No match for latin_name in GBIF.")

        self.gbif_id = species_data["usageKey"]

        if rank == "SPECIES":
            self.genus = _get_genus(species_data)

        elif rank == "GENUS":
            self.family = _get_family(species_data)

    class Meta:
        abstract = True
        ordering = ["latin_name"]


class Family(SpeciesBase):
    """Represents a biological family, which is a higher classification group that contains one or more genera."""

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")

    def enrich_species_data(self):
        super()._enrich_by_name(rank="FAMILY")


class Genus(SpeciesBase):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")

    class Meta:
        verbose_name = _("genus")
        verbose_name_plural = _("genera")

    def enrich_species_data(self):
        super()._enrich_by_name(rank="GENUS")


class Species(SpeciesBase):
    """Represents a biological species with a Latin name."""

    genus = models.ForeignKey(Genus, on_delete=models.PROTECT, related_name="species")

    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")

    def enrich_species_data(self):
        super()._enrich_by_name(rank="SPECIES")


def _get_family(species_data: dict) -> Family:
    """Returns a Family instance based on GBIF species data."""
    try:
        return Family.objects.get(gbif_id=species_data["familyKey"])
    except Family.DoesNotExist:
        return Family.objects.create(
            gbif_id=species_data["familyKey"],
            latin_name=species_data["family"],
        )


def _get_genus(species_data: dict) -> Genus:
    """Returns a Genus instance based on GBIF species data."""
    try:
        return Genus.objects.get(gbif_id=species_data["genusKey"])
    except Genus.DoesNotExist:
        return Genus.objects.create(
            family=_get_family(species_data),
            gbif_id=species_data["genusKey"],
            latin_name=species_data["genus"],
        )


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
