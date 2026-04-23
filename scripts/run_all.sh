#!/bin/bash

# Simple script to run all analysis scripts for RQ2
# Usage: bash scripts/run_all.sh

echo "Running RQ2 Analysis Pipeline..."

echo "1. Filtering humans and bots..."
python3 src/rq2/Filter_by_human_or_bot.py

echo "2. Extracting unique human reviewers..."
python3 src/rq2/Unique_human.py

echo "3. Extracting unique bot reviewers..."
python3 src/rq2/Unique_Bot.py

echo "Pipeline completed."
