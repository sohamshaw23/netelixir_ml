"""
Customer Segmentation Models
============================

Contains

• KMeans Model
"""

from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent

KMEANS_MODEL = (

    MODEL_DIR /

    "kmeans.pkl"

)

__all__ = [

    "MODEL_DIR",

    "KMEANS_MODEL"

]

