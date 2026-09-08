from pydantic import BaseModel, field_validator, model_validator
from typing import List


class LineItem(BaseModel):
    name: str
    quantity: float
    unit_price: float
    line_total: float
    confidence: float = 1.0

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @field_validator("unit_price", "line_total")
    @classmethod
    def price_must_not_be_negative(cls, v):
        if v < 0:
            raise ValueError("Price/total cannot be negative")
        return v

    @field_validator("confidence")
    @classmethod
    def confidence_in_range(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Confidence must be between 0 and 1")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Item name cannot be empty")
        return v


class Bill(BaseModel):
    items: List[LineItem]
    subtotal: float
    subtotal_confidence: float = 1.0
    discount: float = 0
    discount_confidence: float = 1.0
    tax: float = 0
    tax_confidence: float = 1.0
    service_charge: float = 0
    service_charge_confidence: float = 1.0
    printed_total: float
    printed_total_confidence: float = 1.0

    @field_validator(
        "subtotal", "discount", "tax", "service_charge", "printed_total"
    )
    @classmethod
    def amounts_not_negative(cls, v):
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v

    @field_validator(
        "subtotal_confidence", "discount_confidence", "tax_confidence",
        "service_charge_confidence", "printed_total_confidence"
    )
    @classmethod
    def confidence_in_range(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Confidence must be between 0 and 1")
        return v

    @model_validator(mode="after")
    def must_have_at_least_one_item(self):
        if not self.items:
            raise ValueError("Bill must have at least one item")
        return self
