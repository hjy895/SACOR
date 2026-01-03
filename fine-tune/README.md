# Fine-tuning Data

This directory contains data prepared for NLLB fine-tuning in JSONL format.

## Structure

- `base/` - Base dataset configuration
  - `train.jsonl` - Training data
  - `val.jsonl` - Validation data
  - `jsonl/` - Language-specific JSONL files

- `augmented/` - Augmented dataset configuration (with additional reference translations)
  - `train.jsonl` - Training data
  - `val.jsonl` - Validation data
  - `jsonl/` - Language-specific JSONL files

- `ablation/` - Ablation study datasets (missing one language at a time)

- `samples/` - Incrementally growing sample datasets (100, 200, 300, ..., 1000 samples)

## JSONL Format

Each line is a JSON object with the following structure:
```json
{
  "translation": {
    "lang_code": "source text",
    "eng_Latn": "target text"
  }
}
```

