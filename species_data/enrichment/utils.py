from typing import List, NamedTuple, Type

from django.db.models import ManyToManyField, Model

from species_data.fields import DecimalEstimatedRange
from species_data.models.base import CategorizedPlantPropertyBase
from species_data.models.models import SpeciesProperties


class Fields(NamedTuple):
    decimalranges: List[str]
    categories: List[str]


def get_fields(model: Type[Model]) -> Fields:
    # if isinstance(property_field, DecimalEstimatedRange):
    #     logger.debug(f"Adding DecimalRangeField property '{property_field}'.")
    #     field_type = DecimalRangeField

    # # Skip for MVP as we'll need to properly implement ISO durations (including months and years).
    # # elif isinstance(property_field, DurationEstimatedRange):
    # #     logger.debug(f"Adding DecimalRangeField property '{property_field}'.")
    # #     field_type = DurationRangeField

    # elif isinstance(property_field, ManyToManyField) and issubclass(
    #     property_field.related_model, CategorizedPlantPropertyBase
    # ):

    fields = Fields([], [])
    for property_field in SpeciesProperties._meta.get_fields():
        if isinstance(property_field, DecimalEstimatedRange):
            fields.decimalranges.append(property_field.name)
        elif isinstance(property_field, ManyToManyField) and issubclass(
            property_field.related_model, CategorizedPlantPropertyBase
        ):
            fields.categories.append(property_field.name)

    return fields
