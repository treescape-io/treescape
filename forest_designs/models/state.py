import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from treescape.models import UUIDIndexedModel

from .base import KindBase
# from .plant import Plant


class PlantState(KindBase):
    """State of a plant (native, planted, planned, dead, etc.)."""

    class Meta(KindBase.Meta):
        verbose_name = _("plant state")
        verbose_name_plural = _("plant states")


class PlantStateTransition(UUIDIndexedModel):
    """Transition between one plant state and another."""

    plant = models.ForeignKey(
        "Plant",
        on_delete=models.CASCADE,
        related_name="statetransitions",
        db_column="plant_uuid",
    )
    date = models.DateTimeField(
        _("date"),
        help_text=_("Moment of state transition."),
        default=datetime.datetime.now,
    )

    state = models.ForeignKey(
        PlantState,
        help_text=_("State to transition to."),
        on_delete=models.PROTECT,
        db_column="state_uuid",
        related_name="transitions",
    )

    def __str__(self) -> str:
        return f"{self.date} to {self.state}"

    class Meta:
        verbose_name = _("plant state transition")
        verbose_name_plural = _("plant state transitions")
        ordering = ["-date"]
