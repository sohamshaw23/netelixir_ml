"""
customer_segmentation/config.py - Customer Segmentation Configuration
=====================================================================
Marketing Intelligence AI Platform
"""

from shared.constants import KMEANS_MODEL
from settings import KMEANS_PARAMS

KMEANS_MODEL_PATH: str = KMEANS_MODEL
KMEANS_DEFAULT_PARAMS: dict = KMEANS_PARAMS

# Optimal number of clusters (determined via Elbow / Silhouette analysis)
# TODO: Run cluster analysis to determine the best K.
N_CLUSTERS: int = 5

# Features used for clustering
# TODO: Populate after feature engineering and EDA.
SEGMENTATION_FEATURE_COLUMNS: list = []

# Segment labels (update after analysing cluster profiles)
# TODO: Replace with meaningful business labels.
SEGMENT_LABELS: dict = {
    0: "Segment A",
    1: "Segment B",
    2: "Segment C",
    3: "Segment D",
    4: "Segment E",
}

# PCA components for visualisation
PCA_COMPONENTS: int = 2
