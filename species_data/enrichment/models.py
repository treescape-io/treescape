import datetime
import logging
import decimal
import enum

from pprint import pformat
from typing import Tuple, Type, Optional, Set, Any

from django.db.models.fields.related import ManyToManyField
from pydantic import BaseModel, Field, create_model

from species_data.models import SpeciesProperties
from species_data.models.base import CategorizedPlantPropertyBase
from species_data.fields import DecimalEstimatedRange  # , DurationEstimatedRange


logger = logging.getLogger(__name__)


class ConfidenceModel(BaseModel):
    confidence: decimal.Decimal = Field(gt=0, le=1, decimal_places=1, max_digits=5)


class DecimalRangeField(ConfidenceModel):
    minimum: Optional[decimal.Decimal] = Field(None, max_digits=7, decimal_places=2)
    typical: Optional[decimal.Decimal] = Field(None, max_digits=7, decimal_places=2)
    maximum: Optional[decimal.Decimal] = Field(None, max_digits=7, decimal_places=2)


class DurationRangeField(ConfidenceModel):
    minimum: Optional[datetime.timedelta] = None
    typical: Optional[datetime.timedelta] = None
    maximum: Optional[datetime.timedelta] = None


def get_species_data_model() -> Type[BaseModel]:
    """Generates a Pydantic model based on the Django models for plant species data categories."""

    def generate_django_enum(django_model: Type[CategorizedPlantPropertyBase]) -> Any:
        """Generates a string Enum based on the name field of the Django model instances."""
        # Retrieve all distinct name values from the Django model
        objects = django_model.objects.all()

        obj_dict = {obj.slug: obj.slug for obj in objects}

        # Create and return an enum with a name based on the Django model's name
        obj_enum = enum.Enum(f"{django_model.__name__}Enum", obj_dict)
        logger.debug(f"generate_django_enum: {pformat(obj_dict)}")

        return obj_enum

    def generate_django_multiselect_field(
        django_model: Type[CategorizedPlantPropertyBase],
    ) -> Type[BaseModel]:
        """Generates a field allowing the selection of multiple options based on a given Django model."""
        model_enum = generate_django_enum(django_model)

        model = create_model(
            f"{django_model.__name__}Model",
            __base__=ConfidenceModel,
            values=(Set[model_enum], ...),
        )

        return model

    def get_model_field(property_field) -> Optional[Tuple[str, Tuple[Type, Any]]]:
        """Determine the Django model field type based on the property field type."""
        field_type = None
        if isinstance(property_field, DecimalEstimatedRange):
            logger.debug(f"Adding DecimalRangeField property '{property_field}'.")
            field_type = Optional[DecimalRangeField]

        # Skip for MVP as we'll need to properly implement ISO durations (including months and years).
        # elif isinstance(property_field, DurationEstimatedRange):
        #     logger.debug(f"Adding DecimalRangeField property '{property_field}'.")
        #     field_type = DurationRangeField

        elif isinstance(property_field, ManyToManyField) and issubclass(
            property_field.related_model, CategorizedPlantPropertyBase
        ):
            logger.debug(f"Adding multiselect property '{property_field}'.")
            field_type = Optional[
                generate_django_multiselect_field(property_field.related_model)
            ]

        if field_type:
            return property_field.name, (field_type, None)

        return None

    model_fields = {
        result[0]: result[1]
        for property_field in SpeciesProperties._meta.get_fields()
        for result in [get_model_field(property_field)]
        if result is not None
    }

    model = create_model("SpeciesModel", **model_fields)  # type: ignore

    return model
