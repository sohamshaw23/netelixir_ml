"""
scripts/train_all.py - Train All Models
========================================
Marketing Intelligence AI Platform

Orchestrates the full training pipeline for all ML modules sequentially.

Usage
-----
    # Train everything
    python scripts/train_all.py

    # Train specific modules only
    python scripts/train_all.py --modules revenue anomaly

    # Skip a module
    python scripts/train_all.py --skip creative

Available module names: revenue, anomaly, segmentation, creative

TODO:
    - Implement each _train_*() function once ML logic is ready.
    - Add --parallel flag to train modules concurrently.
    - Log metrics to MLflow / W&B after each module.
"""

import argparse
import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path for absolute imports.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

ALL_MODULES = ["revenue", "anomaly", "segmentation", "creative"]


# ---------------------------------------------------------------------------
# Per-module trainers
# ---------------------------------------------------------------------------

def train_revenue_model() -> None:
    """Train the Revenue Drop Risk model. TODO: Implement full pipeline."""
    from revenue_drop_risk.train import RevenueTrainer
    logger.info("[revenue] Starting Revenue Drop Risk training …")
    RevenueTrainer().run()
    logger.info("[revenue] Done.")


def train_anomaly_model() -> None:
    """Train the Anomaly Detection model. TODO: Implement full pipeline."""
    from anomaly_detection.train import AnomalyTrainer
    logger.info("[anomaly] Starting Anomaly Detection training …")
    AnomalyTrainer().run()
    logger.info("[anomaly] Done.")


def train_segmentation_model() -> None:
    """Train the Customer Segmentation model. TODO: Implement full pipeline."""
    from customer_segmentation.train import SegmentationTrainer
    logger.info("[segmentation] Starting Customer Segmentation training …")
    SegmentationTrainer().run()
    logger.info("[segmentation] Done.")


def train_creative_model() -> None:
    """Train the Creative Performance model. TODO: Implement full pipeline."""
    from creative_performance.train import CreativeTrainer
    logger.info("[creative] Starting Creative Performance training …")
    CreativeTrainer().run()
    logger.info("[creative] Done.")


_TRAINER_MAP = {
    "revenue":      train_revenue_model,
    "anomaly":      train_anomaly_model,
    "segmentation": train_segmentation_model,
    "creative":     train_creative_model,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="train_all.py",
        description="Train ML models for the Marketing Intelligence AI Platform.",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=ALL_MODULES,
        default=ALL_MODULES,
        metavar="MODULE",
        help=f"Modules to train (default: all). Choices: {ALL_MODULES}",
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        choices=ALL_MODULES,
        default=[],
        metavar="MODULE",
        help="Modules to skip.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    modules_to_run = [m for m in args.modules if m not in args.skip]

    logger.info("=== Training pipeline started. Modules: %s ===", modules_to_run)

    for module in modules_to_run:
        try:
            _TRAINER_MAP[module]()
        except Exception as exc:
            logger.error("[%s] Training failed: %s", module, exc, exc_info=True)

    logger.info("=== Training pipeline complete ===")


if __name__ == "__main__":
    main()
