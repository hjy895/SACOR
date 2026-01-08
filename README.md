# SACOR: A Multilingual Parallel Corpus for Low-Resource South Asian Languages

** We provide parallel corpora for eight under-represented languages in South Asia along with scripts to fine-tune NLLB. The resources are open-source. Please consider these languages in your projects!**

South Asia is characterized by remarkable linguistic diversity, with over 1.8 billion inhabitants speaking more than 650 languages across multiple language families. In a first attempt of its kind, we create parallel corpora for the following eight under-represented languages of South Asia:

<figure>
  <p align="center">
    <img width="476" height="355" alt="Figure 1: Language distribution map"
         <img width="476" height="355" alt="image" src="https://github.com/user-attachments/assets/e1d886d8-6f54-4230-8f4e-b36ed01afac7" />
  </p>
  <figcaption align="center">
    <b>Figure 1.</b> Map of where major South Asian languages are spoken in Pakistan and nearby regions; overlapping colors show multilingual areas, gray symbols indicate other recorded languages, and red squares mark major cities.
  </figcaption>
</figure> <br>


- **Punjabi** - Shahmukhi-based (Punjab, Pakistan)
- **Pashto** - Native language of Afghanistan and parts of Pakistan
- **Sindhi** - Language of Sindh province with unique character set
- **Saraiki** - Spoken in southern Punjab with distinctive writing system
- **Urdu** - National language of Pakistan, widely spoken across South Asia
- **Balochi** - Language of Balochistan region
- **Hindko** - Language of northern Pakistan, particularly Khyber Pakhtunkhwa
- **Brahui** - Dravidian language spoken in Balochistan

This repository provides documentation on our project that aims to develop machine translation for low-resource languages in South Asia. We use the **NLLB-200-distilled-1.3B** model for fine-tuning, providing better translation quality while maintaining computational efficiency.

**The project couldn't be possible without the enthusiasm and passion of volunteers who contributed to the project by translating sentences. You are free to use everything, but please be mindful to acknowledge the project if you use it. [Read the license](#license).**

## Guidelines for Contributors

If you are interested in contributing translations to this project, please read our guidelines:

- [English Guidelines](Guideline-EN.md)
- [Urdu Guidelines](Guideline-URD.md)
- [Punjabi Guidelines](Guideline-PAN.md)

## Parallel Corpora

All the parallel corpora are provided in the [corpora](corpora) folder. These are TSV files containing parallel sentences in English and the target languages. These files include the following meta-data:

- `en_sentence`: sentence in English
- `target_sentence`: sentence in the target language
- `variety`: variety (dialect) - Standard for all languages
- `region`: approximate region where the translator comes from - South Asia
- `translator`: translator ID (for internal tracking)

When processing these files, you can extract the relevant columns as all the fields in the metadata are not useful for MT.

### Cross-lingual Alignment

Some of the translated sentences are aligned with the same source sentences in English, creating a multilingual parallel corpus ideal for cross-lingual studies. We have merged all sentences across languages based on the English source sentences. This multilingual corpus is available at [corpora/multilingual-corpus.tsv](corpora/multilingual-corpus.tsv) (to be generated). To find the meta-data, you should look up the sentences in the original corpora.

## Data Splits

If you are looking for dataset splits, check out the [datasets](datasets) folder where sentences in the [parallel corpora](corpora) are split into test, validation and train sets. The splits follow a 70/15/15 distribution (train/validation/test) to ensure fair representation across all languages.

### JSONL

All the dataset splits are also available in `jsonlines` format, ready for training/fine-tuning using [Hugging Face](https://huggingface.co/docs/datasets/v3.2.0/loading#json-files). These files are provided in the [fine-tune](fine-tune) folder. The `base` and `augmented` sub-folders refer to different data configurations. Within each folder, you can find the prefixed sentences as well.

The datasets used in the ablation studies are provided in [ablation](fine-tune/ablation) and [samples](fine-tune/samples) folders.

## Summary of Resources

To summarize, these are the available corpora and datasets per language:

| Language | Parallel languages | # Sentence pairs | # Varieties | Download | JSONL |
|----------|---------------------|------------------|-------------|----------|-------|
| **Punjabi** (PAN) | English | 5,127 | Standard | [corpus](corpora/en-pan.tsv) \| [test](datasets/PAN-test.tsv) / [val](datasets/PAN-val.tsv) / [train](datasets/PAN-train.tsv) | [train](fine-tune/base/jsonl/pan_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/pan_Arab-eng_Latn.val.jsonl) |
| **Pashto** (PBT) | English | 5,857 | Standard | [corpus](corpora/en-pbt.tsv) \| [test](datasets/PBT-test.tsv) / [val](datasets/PBT-val.tsv) / [train](datasets/PBT-train.tsv) | [train](fine-tune/base/jsonl/pbt_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/pbt_Arab-eng_Latn.val.jsonl) |
| **Sindhi** (SND) | English | 6,812 | Standard | [corpus](corpora/en-snd.tsv) \| [test](datasets/SND-test.tsv) / [val](datasets/SND-val.tsv) / [train](datasets/SND-train.tsv) | [train](fine-tune/base/jsonl/snd_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/snd_Arab-eng_Latn.val.jsonl) |
| **Saraiki** (SKR) | English | 4,179 | Standard | [corpus](corpora/en-skr.tsv) \| [test](datasets/SKR-test.tsv) / [val](datasets/SKR-val.tsv) / [train](datasets/SKR-train.tsv) | [train](fine-tune/base/jsonl/skr_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/skr_Arab-eng_Latn.val.jsonl) |
| **Urdu** (URD) | English | 7,940 | Standard | [corpus](corpora/en-urd.tsv) \| [test](datasets/URD-test.tsv) / [val](datasets/URD-val.tsv) / [train](datasets/URD-train.tsv) | [train](fine-tune/base/jsonl/urd_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/urd_Arab-eng_Latn.val.jsonl) |
| **Balochi** (BAL) | English | 3,425 | Standard | [corpus](corpora/en-bal.tsv) \| [test](datasets/BAL-test.tsv) / [val](datasets/BAL-val.tsv) / [train](datasets/BAL-train.tsv) | [train](fine-tune/base/jsonl/bal_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/bal_Arab-eng_Latn.val.jsonl) |
| **Hindko** (HND) | English | 2,914 | Standard | [corpus](corpora/en-hnd.tsv) \| [test](datasets/HND-test.tsv) / [val](datasets/HND-val.tsv) / [train](datasets/HND-train.tsv) | [train](fine-tune/base/jsonl/hnd_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/hnd_Arab-eng_Latn.val.jsonl) |
| **Brahui** (BRH) | English | 2,371 | Standard | [corpus](corpora/en-brh.tsv) \| [test](datasets/BRH-test.tsv) / [val](datasets/BRH-val.tsv) / [train](datasets/BRH-train.tsv) | [train](fine-tune/base/jsonl/brh_Arab-eng_Latn.train.jsonl) / [val](fine-tune/base/jsonl/brh_Arab-eng_Latn.val.jsonl) |

**Total: 38,625 parallel sentence pairs across 8 languages**

### Dataset Statistics

- **Training set**: 27,033 sentences (70.0%)
- **Validation set**: 5,790 sentences (15.0%)
- **Test set**: 5,802 sentences (15.0%)

## Scripts

Although it's not the main contribution of the project, we release all the scripts used for preparing the corpora, data splits and fine-tuning. Please note that the codes are not optimized and you might need to change directory of files (it might be easier to simply work with the datasets and the corpora, tbh!). Additional codes are provided in the [utils](utils) folder.

### Corpora

- [`create_corpus.py`](codes/create_corpus.py): Implements semantic and string-based similarity measures to ensure that a diverse set of sentences are extracted from the corpus. Make sure to update [`codes/data.json`](codes/data.json) by specifying the directory of your files.
- [`sentence_extractor.py`](codes/sentence_extractor.py): If you have a monolingual corpus, use this script to extract sentences for translation into a high-resource language.
- [`random_sample.py`](codes/random_sample.py): Randomly selected sentences from a monolingual corpus.

### Prepare datasets and splits

- [`prepare_nllb_data.py`](codes/prepare_nllb_data.py): Prepares datasets for NLLB fine-tuning with both base and augmented configurations.
- [`merge_datasets.py`](codes/merge_datasets.py): Merges all the individual jsonl files into one.
- [`add_lang_prefix.py`](codes/add_lang_prefix.py): Prepends language indicator token to the beginning of each sentence.
- [`sampler_size.py`](codes/sampler_size.py): Samples from the datasets by incrementally selecting sentences per language.
- [`sampler_exclusive.py`](codes/sampler_exclusive.py): Creates samples missing data from a language each time.

### Fine-tuning

- [`fine-tune.py`](codes/fine-tune.py): Initializes [NLLB (1.3B distilled)](https://huggingface.co/facebook/nllb-200-distilled-1.3B) by adding new token indicators for our selected languages. We use the 1.3B model for better translation quality while maintaining computational efficiency.
- [`run_translation.py`](codes/run_translation.py): This is a modified version of [Hugging Face's fine-tuning code](https://raw.githubusercontent.com/huggingface/transformers/refs/heads/main/examples/pytorch/translation/run_translation.py) with the main difference being on tokenization. We remove the source and target language tokens as arguments.
- For more information on fine-tuning NLLB, check [this](https://github.com/huggingface/transformers/tree/main/examples/pytorch/translation#readme) and [this](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/nllb.md).

### Evaluation

- [`evaluate-zero-shot.py`](codes/evaluate-zero-shot.py): Zero-shot evaluation of NLLB
- [`scorer.py`](codes/scorer.py): Calculates BLEU & chrF scores on the output of the zero-shot evaluation
- [`models_evaluate.py`](codes/models_evaluate.py): Evaluates fine-tuned models

## Language Scripts and Orthography

All languages use their correct, standard writing systems as used in Pakistan and South Asia:

- **Punjabi**: Shahmukhi-based (Punjab, Pakistan) - Uses standard writing system for Punjabi in Pakistan
- **Pashto**: Uses Pashto-specific characters (ښ, ډ, etc.) in its writing system
- **Sindhi**: Uses Sindhi-specific characters (ڪ, ڀ, etc.) in its writing system
- **Saraiki**: Uses Saraiki-specific characters (ݙ, ݨ) in its writing system - **correct for Saraiki**
- **Urdu**: Standard writing system used in Pakistan and India
- **Balochi**: Standard writing system for Balochi language
- **Hindko**: Standard writing system for Hindko language
- **Brahui**: Standard writing system for Brahui language

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SACOR-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

For detailed setup instructions, see [SETUP.md](SETUP.md).

## License

This project is fully open-source with the extremely permissive [MIT license](LICENSE). **Please be mindful that there is much effort going into this!**

Any support to sustain this initiative, as well as research collaborations to expand these resources, is welcome. For collaboration inquiries, don't hesitate to reach out.

## Citation

If you're using this project, please cite appropriately:

```bibtex
@misc{sacor2024,
  title = {{SACOR}: A Multilingual Parallel Corpus for Low-Resource {South Asian} Languages},
  author = {SACOR Contributors},
  year = {2024},
  howpublished = {\url{https://github.com/yourusername/SACOR}}
}
```










