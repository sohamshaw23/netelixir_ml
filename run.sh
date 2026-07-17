#!/usr/bin/env bash
# run.sh
# Entry point for the hackathon automated testing pipeline.

set -euo pipefail

# Accept arguments, fall back to defaults for local runs
DATA_DIR="${1:-./data}"
MODEL_PATH="${2:-./pickle/revenue_model.pkl}"
OUTPUT_PATH="${3:-./output/predictions.csv}"

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_PATH")"

# Execute feature engineering and inference pipeline
python3 submission_predict.py "$DATA_DIR" "$MODEL_PATH" "$OUTPUT_PATH"

echo "Done. Predictions written to $OUTPUT_PATH"
