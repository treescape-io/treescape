from pathlib import PurePath
import uuid

from django.contrib.gis.db import models


class UUIDIndexedModel(models.Model):
    """To prevent version conflicts during editing, use uuid's for indexing."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


def uuid_image_path_generator(root_path: PurePath | str):
    root = PurePath(root_path)

    def _species_image_path(instance, filename) -> str:
        ext = PurePath(filename).suffix
        assert getattr(instance, "uuid")
        file_path: PurePath = root / str(instance.uuid)
        return file_path.with_suffix(ext).as_posix()

    return _species_image_path
