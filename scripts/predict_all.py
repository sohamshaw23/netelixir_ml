"""
scripts/predict_all.py - Run All Batch Predictions
===================================================
Marketing Intelligence AI Platform

Runs batch inference for all ML modules using trained model artefacts.

Usage
-----
    # Run all predictions
    python scripts/predict_all.py

    # Run specific modules only
    python scripts/predict_all.py --modules revenue anomaly

    # Specify custom input/output paths
    python scripts/predict_all.py --input data/processed/cleaned_dataset.csv --output data/outputs/

Available module names: revenue, anomaly, segmentation, creative

TODO:
    - Implement each _predict_*() function once inference engines are wired up.
    - Add --format flag to support JSON / parquet output in addition to CSV.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

ALL_MODULES = ["revenue", "anomaly", "segmentation", "creative"]


# ---------------------------------------------------------------------------
# Per-module batch runners
# ---------------------------------------------------------------------------

def predict_revenue(input_path: str = None, output_path: str = None) -> None:
    """Run batch revenue drop risk prediction. TODO: Implement."""
    from revenue_drop_risk.predict import run_batch_prediction
    logger.info("[revenue] Running batch prediction …")
    kwargs = {}
    if input_path:
        kwargs["input_path"] = input_path
    if output_path:
        from shared.constants import REVENUE_RISK_OUTPUT
        kwargs["output_path"] = str(Path(output_path) / Path(REVENUE_RISK_OUTPUT).name)
    run_batch_prediction(**kwargs)
    logger.info("[revenue] Done.")


def detect_anomalies(input_path: str = None, output_path: str = None) -> None:
    """Run batch anomaly detection. TODO: Implement."""
    from anomaly_detection.detect import run_batch_detection
    logger.info("[anomaly] Running batch detection …")
    kwargs = {}
    if input_path:
        kwargs["input_path"] = input_path
    if output_path:
        from shared.constants import ANOMALIES_OUTPUT
        kwargs["output_path"] = str(Path(output_path) / Path(ANOMALIES_OUTPUT).name)
    run_batch_detection(**kwargs)
    logger.info("[anomaly] Done.")


def segment_customers(input_path: str = None, output_path: str = None) -> None:
    """Run batch customer segmentation. TODO: Implement."""
    from customer_segmentation.segment import run_batch_segmentation
    logger.info("[segmentation] Running batch segmentation …")
    kwargs = {}
    if input_path:
        kwargs["input_path"] = input_path
    if output_path:
        from shared.constants import SEGMENTS_OUTPUT
        kwargs["output_path"] = str(Path(output_path) / Path(SEGMENTS_OUTPUT).name)
    run_batch_segmentation(**kwargs)
    logger.info("[segmentation] Done.")


def score_creatives(input_path: str = None, output_path: str = None) -> None:
    """Run batch creative scoring. TODO: Implement."""
    from creative_performance.predict import run_batch_scoring
    logger.info("[creative] Running batch creative scoring …")
    kwargs = {}
    if input_path:
        kwargs["input_path"] = input_path
    if output_path:
        from shared.constants import CREATIVE_SCORES_OUTPUT
        kwargs["output_path"] = str(Path(output_path) / Path(CREATIVE_SCORES_OUTPUT).name)
    run_batch_scoring(**kwargs)
    logger.info("[creative] Done.")


_PREDICTOR_MAP = {
    "revenue":      predict_revenue,
    "anomaly":      detect_anomalies,
    "segmentation": segment_customers,
    "creative":     score_creatives,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="predict_all.py",
        description="Run batch inference for all ML modules.",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=ALL_MODULES,
        default=ALL_MODULES,
        metavar="MODULE",
        help=f"Modules to run (default: all). Choices: {ALL_MODULES}",
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        choices=ALL_MODULES,
        default=[],
        metavar="MODULE",
        help="Modules to skip.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to input CSV file (overrides each module's default).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        metavar="DIR",
        help="Output directory for all prediction CSVs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    modules_to_run = [m for m in args.modules if m not in args.skip]

    logger.info("=== Batch prediction started. Modules: %s ===", modules_to_run)

    for module in modules_to_run:
        try:
            _PREDICTOR_MAP[module](input_path=args.input, output_path=args.output)
        except Exception as exc:
            logger.error("[%s] Prediction failed: %s", module, exc, exc_info=True)

    logger.info("=== Batch prediction complete ===")


if __name__ == "__main__":
    main()
