import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from treescape.models import UUIDIndexedModel

from .base import KindBase
from .plant import Plant


class PlantLogKind(KindBase):
    """Represents a kind of plant log."""

    class Meta(KindBase.Meta):
        verbose_name = _("plant log type")
        verbose_name_plural = _("plant log types")


class PlantLog(UUIDIndexedModel):
    """Represents a chronological record of events related to a plant."""

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="logs")
    date = models.DateTimeField(
        _("date"),
        help_text=_("Timestamp of the log entry."),
        default=datetime.datetime.now,
    )
    kind = models.ForeignKey(PlantLogKind, on_delete=models.PROTECT)
    notes = models.TextField(_("notes"))

    def __str__(self) -> str:
        return f"{self.date} {self.kind} for {self.plant}"

    class Meta:
        verbose_name = _("plant log")
        verbose_name_plural = _("plant logs")
        ordering = ["-date"]
