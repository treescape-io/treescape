from django.contrib.gis.geos import GEOSGeometry
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from forest_designs.models.state import PlantState
from plant_species.models import Genus, Species, SpeciesVariety
from treescape.models import UUIDIndexedModel


class Plant(UUIDIndexedModel):
    """Plant with specific location within design."""

    genus = models.ForeignKey(
        Genus,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="genus_uuid",
        to_field="uuid",
    )
    species = models.ForeignKey(
        Species,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text=_("When specified, genus is automatically set."),
        db_column="species_uuid",
        to_field="uuid",
    )
    variety = models.ForeignKey(
        SpeciesVariety,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("When specified, species and genus are automatically set."),
        db_column="variety_uuid",
        to_field="uuid",
    )

    location = models.PointField(
        _("location"), unique=True, tolerance=0.05, spatial_index=True
    )

    def get_state(self) -> PlantState | None:
        transition = self.statetransitions.first()
        if transition:
            return transition.state
        return None

    def get_name(self) -> str | None:
        """Return plant name, based on the level of detail given."""

        if self.variety_id:  # pyright: ignore reportAttributeAccessIssue
            return str(self.variety)
        if self.species_id:  # pyright: ignore reportAttributeAccessIssue
            return str(self.species)
        if self.genus_id:  # pyright: ignore reportAttributeAccessIssue
            return str(self.genus)

        return None

    def __str__(self) -> str:
        assert isinstance(self.location, GEOSGeometry)
        return f"{self.get_name()} {self.location.coord_seq}"

    def save(self, *args, **kwargs):
        # If variety specified, override species.
        if self.variety:
            self.species = self.variety.species

        # If species specified, override genus.
        if self.species:
            self.genus = self.species.genus

        super().save(*args, **kwargs)

    class Meta:
        # One of species, genus or variety needs to be set.
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(species__isnull=False)
                    | models.Q(genus__isnull=False)
                    | models.Q(variety__isnull=False)
                ),
                name="forest_designs_plant_genus_species_variety_notnull",
            ),
        ]
        verbose_name = _("plant")
        verbose_name_plural = _("plants")
