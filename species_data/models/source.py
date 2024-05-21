import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class SourceType(models.Model):
    """Type of source, e.g. Wikipedia, Trefle, GPT4 etc."""

    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("source type")
        verbose_name_plural = _("source types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Source(models.Model):
    """Source for species data."""

    source_type = models.ForeignKey(
        SourceType,
        on_delete=models.PROTECT,
    )

    name = models.CharField(_("name"), max_length=255)
    date = models.DateField(_("date"), default=datetime.datetime.now)
    url = models.URLField(_("URL"), unique=True)

    class Meta:
        verbose_name = _("source")
        verbose_name_plural = _("sources")
        ordering = ["name"]

    def __str__(self):
        return f"{self.source_type}: {self.name}"
