import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class UUIDIndexedModel(models.Model):
    """To prevent version conflicts during editing, use uuid's for indexing."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class KindBase(UUIDIndexedModel):
    """Base class for kinds of stuff (zones, images, logs)."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]
