import uuid

from django.contrib.gis.db import models


class UUIDIndexedModel(models.Model):
    """To prevent version conflicts during editing, use uuid's for indexing."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
