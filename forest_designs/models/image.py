import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from treescape.models import UUIDIndexedModel, uuid_image_path_generator

from .base import KindBase


class PlantImageKind(KindBase):
    """Represents a kind of plant image."""

    class Meta(KindBase.Meta):
        verbose_name = _("plant image type")
        verbose_name_plural = _("plant image types")


class PlantImage(UUIDIndexedModel):
    """Image of a plant."""

    plant = models.ForeignKey(
        "Plant",
        on_delete=models.CASCADE,
        related_name="images",
        db_column="plant_uuid",
        to_field="uuid",
    )
    date = models.DateTimeField(_("date"), db_index=True, default=datetime.datetime.now)

    kind = models.ForeignKey(
        PlantImageKind,
        on_delete=models.PROTECT,
        db_column="plantimagekind_uuid",
        to_field="uuid",
    )
    image = models.ImageField(
        _("image"), upload_to=uuid_image_path_generator("forest_designs/images/")
    )

    def __str__(self) -> str:
        return f"{self.plant} image"

    class Meta:
        verbose_name = _("plant image")
        verbose_name_plural = _("plant images")
        ordering = ("plant", "-date")
