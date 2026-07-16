"""
models/__init__.py - Models Package
=====================================
Marketing Intelligence AI Platform

Makes the models/ directory an importable Python package and exposes
the central ModelRegistry for easy access to all trained artefacts.
"""

from models.model_registry import ModelRegistry

__all__ = ["ModelRegistry"]
