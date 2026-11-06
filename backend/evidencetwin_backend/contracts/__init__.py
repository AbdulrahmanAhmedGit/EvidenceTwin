"""Pydantic-backed, strict TypedDict wire contracts matching frontend schemas.

Use validate_contract(Schema, payload) and TypeAdapter(Schema).json_schema().
These describe transport data, never scientific truth or storage entities.
"""
from .common import validate_contract

__all__ = ["validate_contract"]
