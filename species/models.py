import pycountry
import abc

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from prettyprinter import cpprint, set_default_style
from pygbif import species

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from species.exceptions import EnrichmentException, SpeciesAlreadyExists
from .exceptions import SpeciesNotFound


set_default_style("light")


def _convert_language_code(alpha_3):
    """Convert ISO 639-2 code to ISO 639-1 using pycountry."""

    assert alpha_3
    country = pycountry.languages.get(alpha_3=alpha_3)
    assert country

    return country.alpha_2


class SpeciesBase(models.Model):
    """Abstract base class for species models."""

    latin_name = models.CharField(_("latin name"), max_length=255, unique=True)
    gbif_id = models.IntegerField(
        _("GBIF usageKey"), null=True, blank=True, unique=True
    )

    def __str__(self):
        """Returns the Latin name of the family."""
        return self.latin_name

    @abc.abstractmethod
    def enrich_data(self):
        pass

    def _enrich_gbif_name(self, rank):
        """Fetch species data from GBIF backbone based on the latin name and updates the instance."""

        assert self.latin_name, "Species name required to enrich data."
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

        if species_data["matchType"] != "EXACT":
            raise SpeciesNotFound(f"No unique match species '{self.latin_name}'.")

        # Use the first non-empty key. Note that synonyms have a different usageKey, so we can't use that.
        self.gbif_id = next(
            filter(
                None,
                (
                    species_data.get("speciesKey"),
                    species_data.get("genusKey"),
                    species_data.get("familyKey"),
                ),
            ),
            None,
        )

        # Use canonical names
        self.latin_name = next(
            filter(
                None,
                (
                    species_data.get("species"),
                    species_data.get("genus"),
                    species_data.get("family"),
                ),
            ),
            None,
        )

        # Validate uniqueness (deal with synonyms)
        try:
            existing_species = self.__class__.objects.get(gbif_id=self.gbif_id)
            raise SpeciesAlreadyExists(
                f"Species '{self.latin_name}' already  exists under name '{existing_species.latin_name}'."
            )
        except ObjectDoesNotExist:
            # All is fine
            pass

        if rank == "SPECIES":
            self.genus = _get_genus(species_data)

        elif rank == "GENUS":
            self.family = _get_family(species_data)

    def enrich_gbif_common_names(self):
        """Fetch (missing) common names from GBIF in configured languages."""
        assert self.pk, "Needs to be saved before adding common names."
        assert self.gbif_id, "GBIF id required to fetch common names."

        names_data = species.name_usage(self.gbif_id, data="vernacularNames")
        enabled_languages = [l[0] for l in settings.LANGUAGES]

        for name_data in names_data["results"]:
            assert "language" in name_data
            assert "vernacularName" in name_data and name_data["vernacularName"]

            if not name_data["language"]:
                continue

            alpha2_lang = _convert_language_code(name_data["language"])
            assert alpha2_lang

            if alpha2_lang in enabled_languages:
                self.common_names.update_or_create(
                    language=alpha2_lang,
                    defaults={
                        "name": name_data["vernacularName"],
                    },
                )

    def clean(self):
        if not self.pk:
            try:
                self.enrich_data()
            except EnrichmentException as e:
                raise ValidationError(e)

        super().clean()

    class Meta:
        abstract = True
        ordering = ["latin_name"]


class Family(SpeciesBase):
    """Represents a biological family, which is a higher classification group that contains one or more genera."""

    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")

    def enrich_data(self):
        self._enrich_gbif_name(rank="FAMILY")


class Genus(SpeciesBase):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")

    class Meta:
        verbose_name = _("genus")
        verbose_name_plural = _("genera")

    def enrich_data(self):
        self._enrich_gbif_name(rank="GENUS")


class Species(SpeciesBase):
    """Represents a biological species with a Latin name."""

    genus = models.ForeignKey(Genus, on_delete=models.PROTECT, related_name="species")

    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")

    def enrich_data(self):
        self._enrich_gbif_name(rank="SPECIES")


@receiver(post_save, sender=Family)
def enrich_family(sender, instance, created, **kwargs):
    if created:
        instance.enrich_gbif_common_names()


@receiver(post_save, sender=Genus)
def enrich_genus(sender, instance, created, **kwargs):
    if created:
        instance.enrich_gbif_common_names()


@receiver(post_save, sender=Species)
def enrich_species(sender, instance, created, **kwargs):
    if created:
        instance.enrich_gbif_common_names()


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

    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="common_names"
    )

    class Meta:
        unique_together = (
            "family",
            "language",
            "name",
        )


class GenusCommonName(CommonNameBase):
    """Represents a common name for a genus in a specific language."""

    genus = models.ForeignKey(
        Genus, on_delete=models.CASCADE, related_name="common_names"
    )

    class Meta:
        unique_together = (
            "genus",
            "language",
            "name",
        )


class SpeciesCommonName(CommonNameBase):
    """Represents a common name for a species in a specific language."""

    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="common_names"
    )

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
