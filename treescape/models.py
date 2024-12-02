import uuid

from django.contrib.gis.db import models


class UUIDIndexedModel(models.Model):
    """To prevent version conflicts during editing, use uuid's for indexing."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
