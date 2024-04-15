import decimal

from pydantic import BaseModel, Field


class DecimalRangeField(BaseModel):
    minimum_value: decimal.Decimal
    typical_value: decimal.Decimal
    maximum_value: decimal.Decimal
    confidence: float = Field(gt=0, lt=1)


class MultiStringDataField(BaseModel):
    selected_values: set[str]
    confidence: float = Field(gt=0, lt=1)


class SpeciesData(BaseModel):
    height: DecimalRangeField = Field(description="plant height (m)")
    width: DecimalRangeField = Field(description="canopy width (m)")
    growth_habits: MultiStringDataField
    # climate_zones: MultiStringDataField = Field(
    #     description="Climate zone(s) for species."
    # )
    human_uses: MultiStringDataField
    ecological_role: MultiStringDataField
