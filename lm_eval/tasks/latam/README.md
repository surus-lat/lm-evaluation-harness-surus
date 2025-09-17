# LATAM Language Tasks

This folder contains group configurations for Latin American language evaluation tasks.

## Structure

The LATAM tasks are organized in a hierarchical structure:

```
latam (top-level group)
├── latam_es (Spanish language group)
│   └── spanish (Spanish language tasks)
│       ├── copa_es
│       ├── escola
│       ├── mgsm_direct_es_spanish_bench
│       ├── openbookqa_es
│       ├── paws_es_spanish_bench
│       ├── teleia (sub-group)
│       │   ├── teleia_cervantes_ave
│       │   ├── teleia_pce
│       │   └── teleia_siele
│       ├── wnli_es
│       └── xnli_es_spanish_bench
└── latam_pr (Portuguese language group)
    └── portuguese (Portuguese language tasks)
        ├── assin2_rte
        ├── assin2_sts
        ├── bluex
        ├── enem_challenge
        └── faquad_nli
```

## Usage

### Run all LATAM tasks:
```bash
python -m lm_eval --tasks latam --model your_model
```

### Run Spanish tasks only:
```bash
python -m lm_eval --tasks latam_es --model your_model
```

### Run Portuguese tasks only:
```bash
python -m lm_eval --tasks latam_pr --model your_model
```

### Run individual language groups:
```bash
python -m lm_eval --tasks spanish --model your_model
python -m lm_eval --tasks portuguese --model your_model
```

## Aggregation

Each group configuration includes metric aggregation:

- **latam**: Aggregates results from latam_es and latam_pr using macro-averaging (weight_by_size: false)
- **latam_es**: Aggregates results from all Spanish tasks using macro-averaging
- **latam_pr**: Aggregates results from all Portuguese tasks using macro-averaging
- **spanish**: Aggregates results from individual Spanish tasks using micro-averaging (weight_by_size: true)
- **portuguese**: Aggregates results from individual Portuguese tasks using micro-averaging (weight_by_size: true)

## Files

- `latam.yaml`: Top-level group configuration
- `latam_es.yaml`: Spanish language group configuration
- `latam_pr.yaml`: Portuguese language group configuration
- `../spanish/spanish.yaml`: Spanish tasks group configuration
- `../portuguese/portuguese.yaml`: Portuguese tasks group configuration

## Version

All group configurations are at version 1.0.

## Fixed Issues

1. **Fixed broken task references**: Updated latam_es.yaml to properly reference the spanish group instead of individual teleia tasks
2. **Fixed broken includes**: Fixed mgsm_direct_es_spanish_bench.yaml which had a broken include reference to disabled tasks
3. **Created proper group hierarchies**: Added spanish.yaml and portuguese.yaml group configurations
4. **Standardized aggregation**: Set up proper metric aggregation at each level

## Individual Task Tags

Individual tasks may retain their original group tags (e.g., `pt_benchmark`, `assin2`, `vestibular`) for backwards compatibility and categorization purposes. These tags do not conflict with the new group structure.