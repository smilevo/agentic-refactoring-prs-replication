# Reproducibility

This repository enables partial and full reproduction of the analyses reported in the paper.

This repository contains the replication package for our study on AI-generated refactoring pull requests in the AIDev dataset.

## Pipeline Overview
1. Normalize pull requests and reviews
2. Extract refactoring action verbs
3. Classify PRs into:
   - Internal quality attributes
   - External quality attributes
   - Code smells
4. Apply review taxonomy coding
5. Generate tables and figures

## Environment
- Python 3.10+
- pandas
- numpy
- regex
- matplotlib
- tqdm

## Quick Run (sample)
```bash
pip install -r requirements.txt
bash scripts/run_all.sh
