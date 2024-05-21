import logging
import requests
import typing

from enum import Enum
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.template.defaultfilters import slugify
from django.db import models, transaction
from django.db.models.query import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import get_language
from django.contrib import admin

from django_advance_thumbnail import AdvanceThumbnailField

from plant_species.enrichment.exceptions import (
    EnrichmentException,
    SpeciesAlreadyExists,
)

from plant_species.enrichment.gbif import (
    get_image_urls,
    get_common_names,
    get_latin_names,
)

from plant_species.enrichment.wikipedia import get_wikipedia_page


logger = logging.getLogger(__name__)


class Rank(Enum):
    FAMILY = "FAMILY"
    GENUS = "GENUS"
    SPECIES = "SPECIES"


class CommonNameBase(models.Model):
    """Abstract base class for common names."""

    language = models.CharField(_("language"), max_length=7, choices=settings.LANGUAGES)
    name = models.CharField(_("common name"), max_length=255, db_index=True)

    is_default = models.BooleanField(
        _("default"), default=False, help_text=_("Use as default name for language.")
    )

    def __str__(self):
        """Returns the common name and its language."""
        return self.name

    class Meta:
        verbose_name = _("common name")
        verbose_name_plural = _("common names")
        ordering = ["language", "-is_default", "name"]
        abstract = True

    def save(self, *args, **kwargs):
        """Ensure there's ever only one default."""
        with transaction.atomic():
            if self.is_default:
                # Set all else to false
                self.__class__.objects.filter(is_default=True).update(is_default=False)

            # The use of return is explained in the comments
            return super().save(*args, **kwargs)


class SpeciesBase(models.Model):
    """Abstract base class for species models."""

    latin_name = models.CharField(
        _("latin name"), max_length=255, unique=True, blank=True
    )
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)
    gbif_id = models.IntegerField(_("GBIF usageKey"), editable=False, unique=True)
    image = models.ImageField(upload_to="plant_species/images/", null=True, blank=True)
    image_thumbnail = AdvanceThumbnailField(  # pyright: ignore[reportCallIssue]
        source_field="image",  # pyright: ignore[reportCallIssue]
        upload_to="plant_species/images/thumbnails/",
        null=True,
        blank=True,
        size=(512, 512),  # pyright: ignore[reportCallIssue]
        editable=False,
    )
    image_large = AdvanceThumbnailField(  # pyright: ignore[reportCallIssue]
        source_field="image",  # pyright: ignore[reportCallIssue]
        upload_to="plant_species/images/large/",
        null=True,
        blank=True,
        size=(2048, 2048),  # pyright: ignore[reportCallIssue]
        editable=False,
    )

    if typing.TYPE_CHECKING:
        from types import MethodType
        from django.db.models.manager import RelatedManager

        common_names: RelatedManager[CommonNameBase]
        enrich_data: MethodType

    def __str__(self):
        """Returns the Latin name of the family."""
        common_name = self.get_common_name()

        if common_name:
            return f"{self.latin_name} ({self.get_common_name()})"

        return self.latin_name

    @admin.display(description=_("Common Name"))
    def get_common_name(self) -> str | None:
        """Return common name for currently used language."""
        current_lang = get_language()

        if not current_lang:
            # Somehow, sometimes this is None, in which case we'll default to English.
            current_lang = "en"

        common_name = self.common_names.filter(
            Q(language=current_lang) | Q(language=current_lang[:2])
        ).first()

        if not common_name:
            return None

        assert isinstance(common_name, CommonNameBase)

        return common_name.name

    @admin.display(
        description="GBIF",
    )
    def gbif_link(self) -> str | None:
        if self.gbif_id:
            return mark_safe(
                f'<a target="_blank" href="https://www.gbif.org/species/{self.gbif_id}/">{self.gbif_id}</a>'
            )

        return _("Not available.")

    @admin.display(
        description="Wikipedia",
    )
    def wikipedia_link(self) -> str | None:
        """Get link for species Wikipedia page."""

        if self.wikipedia_page:
            return mark_safe(
                f'<a target="_blank" href="{self.wikipedia_page.url}">{self.wikipedia_page.title}</a>'
            )
        return _("Not available.")

    # TODO: Query Wikidata
    # Options:
    # a) https://www.gbif.org/api/wikidata/species/2945453?locale=en (undocumented)
    # b) https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fsubject%20WHERE%20%7B%20%3Fsubject%20wdt%3AP846%20%274481106%27%7D
    #    this gets the id, then query the contents
    #    https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q732867&format=json
    # Ref: https://discourse.gbif.org/t/given-a-gbif-human-readable-webpage-for-a-species-how-to-find-the-api-call-for-each-item-on-the-page/3134/11

    @cached_property
    def wikipedia_page(self):
        assert self.latin_name, "latin_name needs to be set"

        return get_wikipedia_page(self.latin_name)

    @admin.display(
        description="Thumbnail",
    )
    def get_thumbnail_html(self) -> str:
        if self.image_thumbnail:
            return mark_safe(
                f'<img src="{self.image_thumbnail.url}" style="height: 128px; width: 128px; object-fit: cover;" alt="Thumbnail of {self}">'
            )
        return _("N/A")

    @admin.display(
        description="Image preview",
    )
    def get_image_html(self) -> str:
        if self.image_large:
            return mark_safe(
                f'<img src="{self.image_large.url}" style="width: 25%" alt="Image of {self}">'
            )
        return _("N/A")

    def enrich_gbif_name(self, rank: Rank):
        """Fetch species data from GBIF backbone based on the latin name and updates the instance."""

        assert self.latin_name, "Species name required to enrich data."
        species_data = get_latin_names(self.latin_name, rank.value)

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

        # Validate uniqueness (deal with synonyms)
        try:
            existing_species = self.__class__.objects.get(gbif_id=self.gbif_id)
            raise SpeciesAlreadyExists(
                f"Species '{self.latin_name}' already  exists under name '{existing_species.latin_name}'."
            )
        except ObjectDoesNotExist:
            # All is fine
            pass

        # Use canonical names
        self.latin_name = next(
            filter(
                None,
                (
                    species_data["species"],
                    species_data["genus"],
                    species_data["family"],
                ),
            ),
            None,
        )

        if rank == "SPECIES":
            self.genus = _get_genus(species_data)

        elif rank == "GENUS":
            self.family = _get_family(species_data)

    def enrich_gbif_image(self):
        """Get image from GBIF and store on `image` field."""
        if self.image:
            # Skip existing images.
            return

        assert isinstance(self.gbif_id, int), "gbif_id not an integer"
        image_urls = get_image_urls(self.gbif_id)

        if image_urls:
            for image_url in image_urls:
                with requests.get(image_url) as response:
                    if response.headers["Content-Type"] not in (
                        "image/jpeg",
                        "image/jpg",
                    ):
                        continue

                    assert self.latin_name
                    image_name = f"{slugify(self.latin_name)}.jpg"
                    image_file = ContentFile(response.content)

                    logger.debug("Saving image %s for %s", image_name, self.latin_name)
                    self.image.save(image_name, image_file)

                    break

    def enrich_gbif_common_names(self):
        """Fetch (missing) common names from GBIF in configured languages."""
        assert self.pk, "Needs to be saved before adding common names."
        assert self.gbif_id, "GBIF id required to fetch common names."

        enabled_languages = [lang[0] for lang in settings.LANGUAGES]

        assert isinstance(self.gbif_id, int), "gbif_id not an integer"
        common_names = get_common_names(self.gbif_id, enabled_languages)

        for name_data in common_names:
            self.common_names.get_or_create(
                language=name_data["language"], name=name_data["name"]
            )

    def enrich_wikipedia(self):
        if not self.description and self.wikipedia_page:
            wikipedia_page = self.wikipedia_page
            if isinstance(wikipedia_page, wikipedia.WikipediaPage):
                logger.debug(
                    "Adding description for %s from Wikipedia", self.latin_name
                )
                self.description = wikipedia_page.summary.strip()

    def clean(self):
        if not self.pk:
            try:
                self.enrich_data()
            except EnrichmentException as e:
                raise ValidationError(e)

        super().clean()

    def save(self, *args, **kwargs):
        if not self.slug:
            assert self.latin_name
            self.slug = slugify(self.latin_name)

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["latin_name"]


class Family(SpeciesBase):
    """Represents a biological family, which is a higher classification group that contains one or more genera."""

    class Meta(SpeciesBase.Meta):
        verbose_name = _("family")
        verbose_name_plural = _("families")

    def enrich_data(self):
        self.enrich_gbif_name(rank=Rank.FAMILY)
        self.enrich_gbif_image()
        self.enrich_wikipedia()


class Genus(SpeciesBase):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")

    class Meta(SpeciesBase.Meta):
        verbose_name = _("genus")
        verbose_name_plural = _("genera")

    def enrich_data(self):
        self.enrich_gbif_name(rank=Rank.GENUS)
        self.enrich_gbif_image()
        self.enrich_wikipedia()


class Species(SpeciesBase):
    """Represents a biological species with a Latin name."""

    genus = models.ForeignKey(Genus, on_delete=models.PROTECT, related_name="species")

    class Meta(SpeciesBase.Meta):
        verbose_name = _("species")
        verbose_name_plural = _("species")

    def enrich_data(self):
        self.enrich_gbif_name(rank=Rank.SPECIES)
        self.enrich_gbif_image()
        self.enrich_wikipedia()


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


class FamilyCommonName(CommonNameBase):
    """Represents a common name for a family in a specific language."""

    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="common_names"
    )

    class Meta(CommonNameBase.Meta):
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

    class Meta(CommonNameBase.Meta):
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

    class Meta(CommonNameBase.Meta):
        unique_together = (
            "species",
            "language",
            "name",
        )


class SpeciesVariety(models.Model):
    """Represents a variety of a species."""

    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="varieties"
    )
    name = models.CharField(_("variety name"), max_length=255, db_index=True)

    def __str__(self):
        """Returns the name of the variety and its species."""
        return f"{self.species} var. {self.name}"

    class Meta:
        verbose_name = _("variety")
        verbose_name_plural = _("varieties")
        ordering = ["species__latin_name", "name"]
        unique_together = (
            "species",
            "name",
        )  # Assuming a species cannot have two varieties with the same name
