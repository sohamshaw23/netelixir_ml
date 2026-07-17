"""
campaign_intelligence sub-package

Exposes API methods for teammate's Integrated LGBM models.
"""

from .inference import (
    predict_revenue_lgbm,
    predict_roas_lgbm,
    predict_campaign_revenue,
    predict_channel_revenue
)
