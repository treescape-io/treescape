import logging
import wikipedia
import requests
import random
import pycountry
import typing

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

from pygbif import species, occurrences
from django_advance_thumbnail import AdvanceThumbnailField

from .exceptions import EnrichmentException, SpeciesAlreadyExists, SpeciesNotFound


logger = logging.getLogger(__name__)


def _convert_language_code(alpha_3):
    """Convert ISO 639-2 code to ISO 639-1 using pycountry."""

    assert alpha_3
    country = pycountry.languages.get(alpha_3=alpha_3)
    assert country

    return country.alpha_2


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

        super().save(*args, **kwargs)

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
        assert self.latin_name

        try:
            page: wikipedia.WikipediaPage = wikipedia.page(
                title=self.latin_name, redirect=True
            )
            return page
        except wikipedia.PageError:
            # Page doesn't exist
            pass
        # except wikipedia.DisambiguationError:
        #     # Page is ambiguous.
        #     pass

        return None

    def get_image_urls(self) -> typing.List[str]:
        """Get URL of CC licensed images."""
        assert self.gbif_id
        occurrence_data = occurrences.search(
            self.gbif_id, mediatype="StillImage", basisOfRecord="HUMAN_OBSERVATION"
        )
        """ Returns something like this:
        {
          "offset":0,
          "limit":2,
          "endOfRecords":false,
          "count":238684,
          "results":[
            {
              "key":4509146329,
              "datasetKey":"963a6b96-4d22-4428-86e4-afee52cf4a8e",
              "publishingOrgKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
              "installationKey":"f9c0c41b-6da4-4be4-b917-a6f7710f3dbc",
              "hostingOrganizationKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
              "publishingCountry":"DK",
              "protocol":"DWC_ARCHIVE",
              "lastCrawled":"2024-04-06T10:26:45.524+00:00",
              "lastParsed":"2024-04-06T10:31:30.950+00:00",
              "crawlId":204,
              "extensions":{
                "http://rs.gbif.org/terms/1.0/Multimedia":[
                  {
                    "http://purl.org/dc/terms/identifier":"https://arter.dk/media/9bf952d1-e004-4a52-bd0f-b0f000e00f61.jpg",
                    "http://purl.org/dc/terms/type":"Image",
                    "http://purl.org/dc/terms/license":"https://creativecommons.org/licenses/by/4.0/"
                  }
                ]
              },
              "basisOfRecord":"HUMAN_OBSERVATION",
              "occurrenceStatus":"PRESENT",
              "taxonKey":5231190,
              "kingdomKey":1,
              "phylumKey":44,
              "classKey":212,
              "orderKey":729,
              "familyKey":5264,
              "genusKey":2492321,
              "speciesKey":5231190,
              "acceptedTaxonKey":5231190,
              "scientificName":"Passer domesticus (Linnaeus, 1758)",
              "acceptedScientificName":"Passer domesticus (Linnaeus, 1758)",
              "kingdom":"Animalia",
              "phylum":"Chordata",
              "order":"Passeriformes",
              "family":"Passeridae",
              "genus":"Passer",
              "species":"Passer domesticus",
              "genericName":"Passer",
              "specificEpithet":"domesticus",
              "taxonRank":"SPECIES",
              "taxonomicStatus":"ACCEPTED",
              "iucnRedListCategory":"LC",
              "decimalLatitude":55.149119,
              "decimalLongitude":12.009073,
              "coordinateUncertaintyInMeters":10.21,
              "continent":"EUROPE",
              "gadm":{
                "level0":{
                  "gid":"DNK",
                  "name":"Denmark"
                },
                "level1":{
                  "gid":"DNK.4_1",
                  "name":"Sjælland"
                },
                "level2":{
                  "gid":"DNK.4.9_1",
                  "name":"Næstved"
                }
              },
              "year":2024,
              "month":1,
              "day":7,
              "eventDate":"2024-01-07",
              "startDayOfYear":7,
              "endDayOfYear":7,
              "issues":[
                "COORDINATE_ROUNDED",
                "CONTINENT_DERIVED_FROM_COORDINATES",
                "TAXON_MATCH_TAXON_ID_IGNORED"
              ],
              "modified":"2024-01-07T17:31:30.725+00:00",
              "lastInterpreted":"2024-04-06T10:31:30.950+00:00",
              "license":"http://creativecommons.org/licenses/by/4.0/legalcode",
              "isSequenced":false,
              "identifiers":[
                {
                  "identifier":"0e098265-8adb-4189-b7e0-b0f000e0100d"
                }
              ],
              "media":[
                {
                  "type":"StillImage",
                  "license":"http://creativecommons.org/licenses/by/4.0/",
                  "identifier":"https://arter.dk/media/9bf952d1-e004-4a52-bd0f-b0f000e00f61.jpg"
                }
              ],
              "facts":[

              ],
              "relations":[

              ],
              "isInCluster":false,
              "recordedBy":"Eddie Bach",
              "identifiedBy":"Eddie Bach",
              "geodeticDatum":"WGS84",
              "class":"Aves",
              "countryCode":"DK",
              "recordedByIDs":[

              ],
              "identifiedByIDs":[

              ],
              "gbifRegion":"EUROPE",
              "country":"Denmark",
              "publishedByGbifRegion":"EUROPE",
              "identifier":"0e098265-8adb-4189-b7e0-b0f000e0100d",
              "catalogNumber":"Arter_0e098265-8adb-4189-b7e0-b0f000e0100d",
              "vernacularName":"Gråspurv",
              "institutionCode":"MST-and-NHMD",
              "dynamicProperties":"{\"Substrate\":\"\"}",
              "eventTime":"14:34:53.268+01:00",
              "gbifID":"4509146329",
              "language":"da",
              "occurrenceID":"https://arter.dk/observation/record-details/0e098265-8adb-4189-b7e0-b0f000e0100d",
              "bibliographicCitation":"Arter.dk Miljøstyrelsen",
              "taxonID":"MSTSNM:Arter:5ebbe02c-52b5-4560-afe2-abc800da0560"
            },
            {
              "key":4509144335,
              "datasetKey":"963a6b96-4d22-4428-86e4-afee52cf4a8e",
              "publishingOrgKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
              "installationKey":"f9c0c41b-6da4-4be4-b917-a6f7710f3dbc",
              "hostingOrganizationKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
              "publishingCountry":"DK",
              "protocol":"DWC_ARCHIVE",
              "lastCrawled":"2024-04-06T10:26:45.524+00:00",
              "lastParsed":"2024-04-06T10:31:33.086+00:00",
              "crawlId":204,
              "extensions":{
                "http://rs.gbif.org/terms/1.0/Multimedia":[
                  {
                    "http://purl.org/dc/terms/identifier":"https://arter.dk/media/5af3c382-9771-4f86-b2bb-b0f300eea47f.jpg",
                    "http://purl.org/dc/terms/type":"Image",
                    "http://purl.org/dc/terms/license":"https://creativecommons.org/licenses/by/4.0/"
                  }
                ]
              },
              "basisOfRecord":"HUMAN_OBSERVATION",
              "occurrenceStatus":"PRESENT",
              "taxonKey":5231190,
              "kingdomKey":1,
              "phylumKey":44,
              "classKey":212,
              "orderKey":729,
              "familyKey":5264,
              "genusKey":2492321,
              "speciesKey":5231190,
              "acceptedTaxonKey":5231190,
              "scientificName":"Passer domesticus (Linnaeus, 1758)",
              "acceptedScientificName":"Passer domesticus (Linnaeus, 1758)",
              "kingdom":"Animalia",
              "phylum":"Chordata",
              "order":"Passeriformes",
              "family":"Passeridae",
              "genus":"Passer",
              "species":"Passer domesticus",
              "genericName":"Passer",
              "specificEpithet":"domesticus",
              "taxonRank":"SPECIES",
              "taxonomicStatus":"ACCEPTED",
              "iucnRedListCategory":"LC",
              "decimalLatitude":54.764569,
              "decimalLongitude":11.867456,
              "coordinateUncertaintyInMeters":18.5,
              "continent":"EUROPE",
              "gadm":{
                "level0":{
                  "gid":"DNK",
                  "name":"Denmark"
                },
                "level1":{
                  "gid":"DNK.4_1",
                  "name":"Sjælland"
                },
                "level2":{
                  "gid":"DNK.4.3_1",
                  "name":"Guldborgsund"
                }
              },
              "year":2024,
              "month":1,
              "day":10,
              "eventDate":"2024-01-10",
              "startDayOfYear":10,
              "endDayOfYear":10,
              "issues":[
                "COORDINATE_ROUNDED",
                "CONTINENT_DERIVED_FROM_COORDINATES",
                "TAXON_MATCH_TAXON_ID_IGNORED"
              ],
              "modified":"2024-01-11T14:27:37.300+00:00",
              "lastInterpreted":"2024-04-06T10:31:33.086+00:00",
              "license":"http://creativecommons.org/licenses/by/4.0/legalcode",
              "isSequenced":false,
              "identifiers":[
                {
                  "identifier":"15ef9233-6298-44cc-9884-b0f300eea4f1"
                }
              ],
              "media":[
                {
                  "type":"StillImage",
                  "license":"http://creativecommons.org/licenses/by/4.0/",
                  "identifier":"https://arter.dk/media/5af3c382-9771-4f86-b2bb-b0f300eea47f.jpg"
                }
              ],
              "facts":[

              ],
              "relations":[

              ],
              "isInCluster":false,
              "recordedBy":"Aske Keiser-Nielsen",
              "identifiedBy":"Aske Keiser-Nielsen",
              "geodeticDatum":"WGS84",
              "class":"Aves",
              "countryCode":"DK",
              "recordedByIDs":[

              ],
              "identifiedByIDs":[

              ],
              "gbifRegion":"EUROPE",
              "country":"Denmark",
              "publishedByGbifRegion":"EUROPE",
              "identifier":"15ef9233-6298-44cc-9884-b0f300eea4f1",
              "catalogNumber":"Arter_15ef9233-6298-44cc-9884-b0f300eea4f1",
              "vernacularName":"Gråspurv",
              "institutionCode":"MST-and-NHMD",
              "dynamicProperties":"{\"Substrate\":\"\"}",
              "eventTime":"15:28:07.796+01:00",
              "gbifID":"4509144335",
              "language":"da",
              "occurrenceID":"https://arter.dk/observation/record-details/15ef9233-6298-44cc-9884-b0f300eea4f1",
              "bibliographicCitation":"Arter.dk Miljøstyrelsen",
              "taxonID":"MSTSNM:Arter:5ebbe02c-52b5-4560-afe2-abc800da0560"
            }
          ],
          "facets":[

          ]
        }
        """
        valid_licenses = (
            # CC-BY
            "http://creativecommons.org/licenses/by/4.0/legalcode",
            "http://creativecommons.org/licenses/by/4.0/",
            "https://creativecommons.org/licenses/by/4.0/deed.en",
            # CC0
            "http://creativecommons.org/publicdomain/zero/1.0/legalcode",
            "http://creativecommons.org/publicdomain/zero/1.0/",
            # CC-BY-SA
            "http://creativecommons.org/licenses/by-sa/4.0/",
        )

        results = occurrence_data["results"]
        assert isinstance(results, list)

        random.shuffle(results)  # Random image for lulz

        def _get_image_url(occurrence: dict) -> str | None:
            for media in occurrence.get("media", []):
                if (
                    media.get("type") == "StillImage"
                    and media.get("license") in valid_licenses
                ):
                    return media.get("identifier")

            return None

        return [url for url in map(_get_image_url, results) if url is not None]

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

    def enrich_gbif_name(self, rank):
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
                    species_data.get("species"),
                    species_data.get("genus"),
                    species_data.get("family"),
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

        image_urls = self.get_image_urls()

        if image_urls:
            for image_url in image_urls:
                with requests.get(image_url) as response:
                    assert self.latin_name
                    if not response.headers["Content-Type"] in (
                        "image/jpeg",
                        "image/jpg",
                    ):
                        continue

                    image_name = f"{slugify(self.latin_name)}.jpg"
                    image_file = ContentFile(response.content)

                    logger.debug("Saving image %s for %s", image_name, self.latin_name)
                    self.image.save(image_name, image_file)

                    break

    def enrich_gbif_common_names(self):
        """Fetch (missing) common names from GBIF in configured languages."""
        assert self.pk, "Needs to be saved before adding common names."
        assert self.gbif_id, "GBIF id required to fetch common names."

        names_data = species.name_usage(self.gbif_id, data="vernacularNames")

        assert isinstance(names_data, dict)
        results = names_data["results"]

        enabled_languages = [lang[0] for lang in settings.LANGUAGES]

        assert isinstance(results, list)
        for name_data in results:
            assert isinstance(name_data, dict)
            assert "language" in name_data
            assert "vernacularName" in name_data and name_data["vernacularName"]

            if not name_data["language"]:
                continue

            alpha2_lang = _convert_language_code(name_data["language"])
            assert alpha2_lang

            if alpha2_lang in enabled_languages:
                self.common_names.get_or_create(
                    language=alpha2_lang, name=name_data["vernacularName"]
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
        self.enrich_gbif_name(rank="FAMILY")
        self.enrich_gbif_image()
        self.enrich_wikipedia()


class Genus(SpeciesBase):
    """Represents a biological genus, which is a group containing one or more species."""

    family = models.ForeignKey(Family, on_delete=models.PROTECT, related_name="genera")

    class Meta(SpeciesBase.Meta):
        verbose_name = _("genus")
        verbose_name_plural = _("genera")

    def enrich_data(self):
        self.enrich_gbif_name(rank="GENUS")
        self.enrich_gbif_image()
        self.enrich_wikipedia()


class Species(SpeciesBase):
    """Represents a biological species with a Latin name."""

    genus = models.ForeignKey(Genus, on_delete=models.PROTECT, related_name="species")

    class Meta(SpeciesBase.Meta):
        verbose_name = _("species")
        verbose_name_plural = _("species")

    def enrich_data(self):
        self.enrich_gbif_name(rank="SPECIES")
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
