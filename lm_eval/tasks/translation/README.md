# Translation Tasks

This folder contains translation evaluation tasks using the FLORES+ dataset for LATAM languages.

## Structure

The translation tasks are organized as follows:

```
translation/
├── translation.yaml                    # Main group: all LATAM translation tasks
├── translation_core.yaml              # Core group: Spanish <-> Portuguese only
├── translation_spanish.yaml           # Spanish group: all languages <-> Spanish
├── translation_portuguese.yaml        # Portuguese group: all languages <-> Portuguese
└── flores_plus_latam/                 # Individual task files
    ├── _flores_plus_common.yaml       # Base configuration
    ├── create_yamls_flores_plus_latam.py  # Script to generate task files
    └── flores_plus_*.yaml             # Individual language pair tasks
```

## Usage

### Run all translation tasks:
```bash
python -m lm_eval --tasks translation --model your_model
```

### Run core translation tasks (Spanish <-> Portuguese only):
```bash
python -m lm_eval --tasks translation_core --model your_model
```

### Run Spanish translation tasks (all languages <-> Spanish):
```bash
python -m lm_eval --tasks translation_spanish --model your_model
```

### Run Portuguese translation tasks (all languages <-> Portuguese):
```bash
python -m lm_eval --tasks translation_portuguese --model your_model
```

### Run individual language pair:
```bash
python -m lm_eval --tasks flores_plus_spa-por --model your_model
```

## Language Pairs

The translation tasks cover the following language pairs:

### Core LATAM Languages
- Spanish ↔ Portuguese

### Extended Language Pairs
- Spanish ↔ English, French, Italian, German, Catalan, Basque, Galician
- Portuguese ↔ English, French, Italian, German, Catalan, Basque, Galician

## Metrics

Each task is evaluated using:
- **BLEU**: Measures n-gram overlap between generated and reference text
- **TER**: Translation Error Rate (lower is better)
- **CHRF**: Character-level F-score for translation quality

## Dataset

The tasks use the [FLORES+ dataset](https://huggingface.co/datasets/openlanguagedata/flores_plus) which provides:
- Parallel sentences in 200+ languages
- Dev and devtest splits (devtest used for evaluation)
- High-quality human translations from Wikinews, Wikijunior, and Wikivoyage

## Task Generation

To regenerate the individual task files, run:
```bash
cd flores_plus_latam/
python3 create_yamls_flores_plus_latam.py --output-dir .
```

## Aggregation

- **translation**: Aggregates results from all language pairs using macro-averaging
- **translation_core**: Aggregates results from Spanish-Portuguese pairs only
- **translation_spanish**: Aggregates results from all Spanish-related pairs
- **translation_portuguese**: Aggregates results from all Portuguese-related pairs
