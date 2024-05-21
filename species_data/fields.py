from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from composite_field import CompositeField


class ConfidenceField(models.DecimalField):
    """Custom FloatField to represent confidence levels with default parameters."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "verbose_name",
            _("confidence"),
        )
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("max_digits", 2)
        kwargs.setdefault("decimal_places", 1)
        kwargs.setdefault(
            "validators", [MinValueValidator(0.0), MaxValueValidator(1.0)]
        )

        super().__init__(*args, **kwargs)


class SourceField(models.ForeignKey):
    """Custom ForeignKey field linking to 'species_data.Source'."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "verbose_name",
            _("source"),
        )
        kwargs.setdefault("to", "species_data.Source")
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)

        # Disable related name (reverse accessor) so it doesn't clash.
        kwargs.setdefault("related_name", "+")

        super().__init__(*args, **kwargs)


class DecimalEstimatedRange(CompositeField):
    """
    Field representing an integer range estimate.

    It consists of the following 'sub' fields:
    - minimum
    - typical
    - maximum
    - confidence (DecimalField, range 0-1)
    """

    minimum = models.DecimalField(
        _("%(parent_verbose_name)s minimum"),
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=1,
    )
    typical = models.DecimalField(
        _("%(parent_verbose_name)s typical"),
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=1,
    )
    maximum = models.DecimalField(
        _("%(parent_verbose_name)s maximum"),
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=1,
    )
    confidence = ConfidenceField(verbose_name=_("%(parent_verbose_name)s confidence"))  # pyright: ignore[reportCallIssue]
    source = SourceField(verbose_name=_("%(parent_verbose_name)s source"))  # pyright: ignore[reportCallIssue]


class DurationEstimatedRange(CompositeField):
    """
    Field representing a duration range estimate.

    It consists of the following 'sub' fields:
    - minimum
    - typical
    - maximum
    - confidence (FloatField, range 0-1)
    """

    minimum = models.DurationField(
        _("%(parent_verbose_name)s minimum"),
        null=True,
        blank=True,
    )
    typical = models.DurationField(
        _("%(parent_verbose_name)s typical"),
        null=True,
        blank=True,
    )
    maximum = models.DurationField(
        _("%(parent_verbose_name)s maximum"),
        null=True,
        blank=True,
    )
    confidence = ConfidenceField(verbose_name=_("%(parent_verbose_name)s confidence"))
    source = SourceField(verbose_name=_("%(parent_verbose_name)s source"))  # pyright: ignore[reportCallIssue]
