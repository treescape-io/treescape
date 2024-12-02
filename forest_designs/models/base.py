from django.db import models
from django.utils.translation import gettext_lazy as _

from treescape.models import UUIDIndexedModel


class KindBase(UUIDIndexedModel):
    """Base class for kinds of stuff (zones, images, logs)."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]
