import decimal
import enum

from typing import Type, Optional, Set, Any

from django.db.models import Model as DjangoModel
from django.utils.text import slugify

from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from species_data.models import GrowthHabit, HumanUse, EcologicalRole, ClimateZone


def get_species_data_model():
    """Generates a Pydantic model based on the Django models for plant species data categories."""

    class ConfidenceModel(BaseModel):
        confidence: decimal.Decimal = Field(gt=0, lt=1, decimal_places=1, max_digits=2)

    class DecimalRangeField(ConfidenceModel):
        minimum: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)
        typical: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)
        maximum: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)

    def generate_django_enum(django_model: Type[DjangoModel]) -> Any:
        """Generates a string Enum based on the name field of the Django model instances."""
        # Retrieve all distinct name values from the Django model
        objects = django_model.objects.all()

        # Create a dictionary for enum where the keys and values are both slugified names of the objects
        obj_dict = {slugify(str(obj)): slugify(str(obj)) for obj in objects}

        # Create and return an enum with a name based on the Django model's name
        obj_enum = enum.Enum(f"{django_model.__name__}Enum", obj_dict)
        return obj_enum

    def generate_django_multiselect_field(django_model: Type[DjangoModel]):
        """Generates a field allowing the selection of multiple options based on a given Django model."""
        model_enum = generate_django_enum(django_model)

        model = create_model(
            f"{django_model.__name__}Model",
            __base__=ConfidenceModel,
            values=(Set[model_enum], ...),
        )

        return model

    class BaseSpeciesData(BaseModel):
        # TODO: Generate all these fields by iterating over the models.
        height: DecimalRangeField = Field(description="mature plant height in meters")
        width: DecimalRangeField = Field(
            description="mature plant canopy diameter in meters"
        )

    model = create_model(
        "SpeciesData",
        __base__=BaseSpeciesData,
        growth_habits=(generate_django_multiselect_field(GrowthHabit), ...),
        human_uses=(generate_django_multiselect_field(HumanUse), ...),
        ecological_roles=(generate_django_multiselect_field(EcologicalRole), ...),
        climate_zones=(generate_django_multiselect_field(ClimateZone), ...),
    )

    return model
