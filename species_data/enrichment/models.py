import decimal
import enum

from typing import Optional

from django.utils.text import slugify

from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from species_data.models import GrowthHabit, HumanUse, EcologicalRole, ClimateZone


def get_species_data_model():
    """Generates a Pydantic model based on the Django models for plant species data categories."""

    class ConfidenceModel(BaseModel):
        confidence: decimal.Decimal = Field(gt=0, lt=1, decimal_places=1, max_digits=2)

    class DecimalRangeField(ConfidenceModel):
        minimum: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)
        typical: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)
        maximum: Optional[decimal.Decimal] = Field(max_digit=3, decimal_places=1)

    def generate_django_enum(model) -> enum.Enum:
        """Generates a string Enum based on the name field of MyModel instances."""
        # Retrieve all distinct name values from MyModel
        objects = model.objects.all()

        obj_dict = {slugify(obj): slugify(obj) for obj in objects}
        obj_enum = enum.Enum(f"{model.__name__}Enum", obj_dict)
        return obj_enum

    def generate_django_multiselect_field(model):
        """Generates a field allowing the selection of multiple options based on a given Django model."""
        model_enum = generate_django_enum(model)
        model = create_model(
            f"{model.__name__}Model",
            __base__=ConfidenceModel,
            values=(set[model_enum], ...),
        )

        return model

    class SpeciesData(BaseModel):
        # TODO: Generate all these fields by iterating over the models.
        height: DecimalRangeField = Field(description="mature plant height in meters")
        width: DecimalRangeField = Field(
            description="mature plant canopy diameter in meters"
        )

        growth_habits: generate_django_multiselect_field(GrowthHabit)
        human_uses: generate_django_multiselect_field(HumanUse)
        ecological_roles: generate_django_multiselect_field(EcologicalRole)
        climate_zones: generate_django_multiselect_field(ClimateZone)

    return SpeciesData
