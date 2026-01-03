# PARUR Setup Guide

## Overview

PARUR (Parallel Corpus for Diverse Low-Resource South Asian Languages) is a repository for creating and fine-tuning machine translation models for eight South Asian languages.

## Languages Supported

1. **Punjabi** (PAN) - `pan_Arab` (Shahmukhi-based, Punjab, Pakistan)
2. **Pashto** (PBT) - `pbt_Arab`
3. **Sindhi** (SND) - `snd_Arab`
4. **Saraiki** (SKR) - `skr_Arab`
5. **Urdu** (URD) - `urd_Arab`
6. **Balochi** (BAL) - `bal_Arab`
7. **Hindko** (HND) - `hnd_Arab`
8. **Brahui** (BRH) - `brh_Arab`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PARUR-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Prepare Your Data

Place your parallel corpora in the `corpora/` directory. Each corpus should be a TSV file with:
- Column 1: English sentences
- Column 2: Target language sentences
- Additional columns: metadata (optional)

### 2. Create Corpus

Use `codes/create_corpus.py` to process your parallel data:
```bash
cd codes
python create_corpus.py
```

Make sure to update `codes/data.json` with your file paths first.

### 3. Prepare Datasets

Split your corpora into train/val/test sets and prepare for NLLB:
```bash
python prepare_nllb_data.py
```

### 4. Extend NLLB Model

Add new language tokens to the NLLB model:
```bash
python fine-tune.py
```

This creates an extended model in `nllb_extended/` directory.

### 5. Fine-tune Model

Fine-tune the extended NLLB model:
```bash
python run_translation.py \
  --model_name_or_path ./nllb_extended \
  --do_train \
  --do_eval \
  --train_file ../fine-tune/base/train.jsonl \
  --validation_file ../fine-tune/base/val.jsonl \
  --output_dir ./nllb_finetuned_base \
  --per_device_train_batch_size 16 \
  --learning_rate 5e-4 \
  --num_train_epochs 20 \
  --warmup_ratio 0.15 \
  --fp16 \
  --predict_with_generate \
  --max_source_length 128 \
  --max_target_length 128 \
  --pad_to_max_length \
  --num_beams 5 \
  --weight_decay 0.01 \
  --seed 42 \
  --overwrite_output_dir
```

### 6. Evaluate Model

Evaluate your fine-tuned model:
```bash
python models_evaluate.py
```

## Directory Structure

```
PARUR-main/
├── codes/              # Python scripts
├── corpora/            # Parallel corpora (TSV files)
├── datasets/            # Train/val/test splits
├── fine-tune/           # JSONL files for training
├── experiments/         # Model outputs and results
├── utils/               # Utility scripts
├── README.md            # Main documentation
├── SETUP.md             # This file
├── requirements.txt     # Python dependencies
└── LICENSE             # MIT License
```

## Notes

- Some languages may need to be added to NLLB tokenizer if they don't exist. The `fine-tune.py` script handles this.
- Update language codes in scripts if your NLLB codes differ from the defaults.
- The repository structure mirrors the original PARME project but adapted for South Asian languages.

## Citation

If you use this repository, please cite appropriately and acknowledge the contributors.

