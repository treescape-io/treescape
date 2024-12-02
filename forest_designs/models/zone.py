from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from treescape.models import UUIDIndexedModel


from .base import KindBase


class ZoneKind(KindBase):
    """Kind of zone within a forest design."""

    class Meta(KindBase.Meta):
        verbose_name = _("zone type")
        verbose_name_plural = _("zone types")


class Zone(UUIDIndexedModel):
    """Zone within a forest design."""

    kind = models.ForeignKey(ZoneKind, on_delete=models.PROTECT)
    name = models.CharField(_("name"), max_length=255)
    area = models.MultiPolygonField(_("area"), spatial_index=True)

    def __str__(self) -> str:
        return f"{self.name} {self.kind}"

    class Meta:
        verbose_name = _("zone")
        verbose_name_plural = _("zones")
        ordering = ["name"]
