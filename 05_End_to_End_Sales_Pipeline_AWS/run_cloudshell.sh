#!/usr/bin/env bash
# Run in AWS CloudShell in eu-north-1 after extracting the deployment bundle.
set -euo pipefail
cd "$(dirname "$0")"
BUCKET=cjb-retail-pipeline
REGION=eu-north-1
SOURCE_KEY="${1:-Raw/Online_Retail.csv}"
RUN_WORK=$(mktemp -d)
echo "Downloading s3://$BUCKET/$SOURCE_KEY"
aws s3 cp "s3://$BUCKET/$SOURCE_KEY" "$RUN_WORK/Online_Retail.csv" --region "$REGION" --only-show-errors
python3 python/retail_pipeline.py --input "$RUN_WORK/Online_Retail.csv" --output "$RUN_WORK/output"
RUN_DIR=$(find "$RUN_WORK/output" -mindepth 1 -maxdepth 1 -type d)
RUN_ID=$(basename "$RUN_DIR")
PREFIX="Processed/runs/$RUN_ID/"
EXISTING=$(aws s3api list-objects-v2 --bucket "$BUCKET" --prefix "$PREFIX" --max-keys 1 --query KeyCount --output text --region "$REGION")
if [ "$EXISTING" != "0" ]; then
  echo "S3 output already exists at $PREFIX. Reuse that completed run; no objects were overwritten."
  echo "Local results: $RUN_DIR"
  exit 1
fi
# Keep the completion report last so partial uploads are distinguishable.
aws s3 cp "$RUN_DIR/" "s3://$BUCKET/$PREFIX" --recursive --exclude 'quality_report.json' --sse AES256 --region "$REGION" --only-show-errors
aws s3 cp "$RUN_DIR/reports/quality_report.json" "s3://$BUCKET/${PREFIX}reports/quality_report.json" --sse AES256 --region "$REGION" --only-show-errors
echo "Completed upload: s3://$BUCKET/$PREFIX"
echo "Copy the following setup statements individually into Athena (eu-north-1):"
cat "$RUN_DIR/athena_setup.sql"
echo "Business queries are in sql/business_queries.sql. Local run files: $RUN_DIR"
