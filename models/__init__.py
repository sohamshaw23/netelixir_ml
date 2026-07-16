"""
models
======

Central Model Package

Provides access to all trained models and preprocessing
artifacts through a single registry.

Author : Team AIgnition
Version : 1.0.0
"""

############################################################
# Registry
############################################################

from .model_registry import (
    ModelRegistry,
    registry
)

############################################################

__version__ = "1.0.0"

############################################################

__all__ = [

    "ModelRegistry",

    "registry"

]

