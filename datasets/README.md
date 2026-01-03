# Dataset Splits

This directory contains train/validation/test splits for each language.

## File Naming Convention

Files are named as `{LANG}-{SPLIT}.tsv` where:
- `LANG` is the language code (PAN, PBT, SND, SKR, URD, BAL, HND, BRH)
- `SPLIT` is one of: `train`, `val`, `test`

## Structure

Each TSV file has the following structure:
- Column 1: English sentence
- Column 2: Target language sentence
- Additional columns: metadata (if applicable)

## Languages

- PAN - Punjabi
- PBT - Pashto
- SND - Sindhi
- SKR - Saraiki
- URD - Urdu
- BAL - Balochi
- HND - Hindko
- BRH - Brahui

