"""Claim-specific development schema, independent of the legacy verifier schema."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

UNITS = {"stress": "MPa", "displacement": "mm", "force": "N"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Observation(StrictModel):
    observable: Literal["stress", "displacement", "force"]
    unit: Literal["MPa", "mm", "N"]
    absolute_tolerance: float = Field(ge=0)

    @model_validator(mode="after")
    def units_match(self):
        if self.unit != UNITS[self.observable]:
            raise ValueError("observable and canonical unit disagree")
        return self


class Claim(Observation):
    id: str = Field(min_length=1)
    decision_rule: Literal["within_reference_tolerance"]


class Case(StrictModel):
    source_case: str = Field(min_length=1)
    loading_convention: Literal["force", "displacement"]


class Explanation(StrictModel):
    id: str = Field(min_length=1)
    source_variant: str = Field(min_length=1)


class Study(StrictModel):
    schema_version: Literal[1]
    scope: str = Field(min_length=1)
    assumptions: list[str] = Field(min_length=1)
    cases: list[Case] = Field(min_length=1)
    claims: list[Claim] = Field(min_length=1)
    allowed_explanations: list[Explanation] = Field(min_length=1)
    observations: list[Observation] = Field(min_length=1)
    evidence_source_variant: str = Field(min_length=1)

    @model_validator(mode="after")
    def identifiers_are_unique(self):
        for items, attr in ((self.cases, "source_case"), (self.claims, "id"),
                            (self.allowed_explanations, "id"), (self.observations, "observable")):
            keys = [getattr(item, attr) for item in items]
            if len(keys) != len(set(keys)):
                raise ValueError(f"duplicate {attr}")
        return self
