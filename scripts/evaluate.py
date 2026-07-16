"""
scripts/evaluate.py - Model Evaluation Script
==============================================
Marketing Intelligence AI Platform

Evaluates all trained models on the test set and prints a comprehensive
metrics report. Optionally saves the report to a JSON file.

Usage
-----
    # Evaluate all modules
    python scripts/evaluate.py

    # Evaluate specific modules
    python scripts/evaluate.py --modules revenue anomaly

    # Save metrics report to a file
    python scripts/evaluate.py --report reports/eval_report.json

    # Evaluate against a custom test set
    python scripts/evaluate.py --test-data data/processed/test.csv

Available module names: revenue, anomaly, segmentation, creative

Steps per module
----------------
    1. Load test data from data/processed/test.csv.
    2. Load trained model artefact via ModelRegistry.
    3. Run inference on test set.
    4. Compute module-appropriate metrics.
    5. Log and (optionally) save results.

TODO:
    - Implement each _evaluate_*() function once models are trained.
    - Add threshold optimisation for the revenue risk classifier.
    - Add confusion matrix and ROC curve generation.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

ALL_MODULES = ["revenue", "anomaly", "segmentation", "creative"]


# ---------------------------------------------------------------------------
# Per-module evaluators
# ---------------------------------------------------------------------------

def evaluate_revenue(test_data_path: str) -> Dict[str, Any]:
    """
    Evaluate the Revenue Drop Risk model on the test set.

    Returns
    -------
    dict: accuracy, precision, recall, f1, roc_auc

    TODO: Implement.
    """
    logger.info("[revenue] Evaluating Revenue Drop Risk model … TODO: Implement.")
    # TODO: Load test data → load model → predict → compute classification metrics.
    return {"module": "revenue", "status": "TODO", "metrics": {}}


def evaluate_anomaly(test_data_path: str) -> Dict[str, Any]:
    """
    Evaluate the Anomaly Detection model against labelled test data.

    Returns
    -------
    dict: precision, recall, f1 for anomaly class

    TODO: Implement.
    """
    logger.info("[anomaly] Evaluating Anomaly Detection model … TODO: Implement.")
    # TODO: Load labelled anomaly test data → predict → compute anomaly metrics.
    return {"module": "anomaly", "status": "TODO", "metrics": {}}


def evaluate_segmentation(test_data_path: str) -> Dict[str, Any]:
    """
    Evaluate the Customer Segmentation model (unsupervised metrics).

    Returns
    -------
    dict: silhouette_score, inertia

    TODO: Implement.
    """
    logger.info("[segmentation] Evaluating Customer Segmentation model … TODO: Implement.")
    # TODO: Load test features → assign clusters → compute silhouette score.
    return {"module": "segmentation", "status": "TODO", "metrics": {}}


def evaluate_creative(test_data_path: str) -> Dict[str, Any]:
    """
    Evaluate the Creative Performance model on the test set.

    Returns
    -------
    dict: mae, rmse, r2

    TODO: Implement.
    """
    logger.info("[creative] Evaluating Creative Performance model … TODO: Implement.")
    # TODO: Load test data → predict → compute regression metrics.
    return {"module": "creative", "status": "TODO", "metrics": {}}


_EVALUATOR_MAP = {
    "revenue":      evaluate_revenue,
    "anomaly":      evaluate_anomaly,
    "segmentation": evaluate_segmentation,
    "creative":     evaluate_creative,
}


# ---------------------------------------------------------------------------
# Report helpers
# ---------------------------------------------------------------------------

def print_report(results: Dict[str, Any]) -> None:
    """Pretty-print the evaluation report to stdout."""
    print("\n" + "=" * 60)
    print("  MARKETING INTELLIGENCE AI — EVALUATION REPORT")
    print(f"  Generated: {results['generated_at']}")
    print("=" * 60)
    for module, data in results["modules"].items():
        print(f"\n  [{module.upper()}]  status={data['status']}")
        metrics = data.get("metrics", {})
        if metrics:
            for metric, value in metrics.items():
                print(f"    {metric:<20} {value}")
        else:
            print("    (no metrics yet — TODO)")
    print("\n" + "=" * 60 + "\n")


def save_report(results: Dict[str, Any], path: str) -> None:
    """Save the evaluation report as JSON."""
    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    logger.info("Evaluation report saved to %s", path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="evaluate.py",
        description="Evaluate trained ML models on the test set.",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=ALL_MODULES,
        default=ALL_MODULES,
        metavar="MODULE",
        help=f"Modules to evaluate (default: all). Choices: {ALL_MODULES}",
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
        "--test-data",
        type=str,
        default="data/processed/test.csv",
        metavar="PATH",
        help="Path to test CSV file (default: data/processed/test.csv).",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to save the JSON evaluation report (optional).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    modules_to_run = [m for m in args.modules if m not in args.skip]

    logger.info("=== Evaluation started. Modules: %s ===", modules_to_run)

    results: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(),
        "test_data":    args.test_data,
        "modules":      {},
    }

    for module in modules_to_run:
        try:
            result = _EVALUATOR_MAP[module](args.test_data)
            results["modules"][module] = result
        except Exception as exc:
            logger.error("[%s] Evaluation failed: %s", module, exc, exc_info=True)
            results["modules"][module] = {"module": module, "status": "ERROR", "error": str(exc)}

    print_report(results)

    if args.report:
        save_report(results, args.report)

    logger.info("=== Evaluation complete ===")


if __name__ == "__main__":
    main()
