from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class KindBase(models.Model):
    """Base class for kinds of stuff (zones, images, logs)."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]
