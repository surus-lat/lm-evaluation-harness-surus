#!/usr/bin/env python3
"""
Generate individual task YAML files for each bidirectional language pair.
"""

import os
from pathlib import Path

# LATAM-focused language pairs (same logic as build_dataset.py)
LANGUAGES = ['spa', 'por', 'eng', 'fra', 'ita', 'deu', 'hin', 'cmn', 'arb']

LANGUAGE_PAIRS = []

# All languages <-> Spanish (excluding Spanish itself)
for lang in LANGUAGES:
    if lang != 'spa':
        LANGUAGE_PAIRS.append(('spa', lang))

# All languages <-> Portuguese (excluding Portuguese itself and Spanish - already covered above)
for lang in LANGUAGES:
    if lang != 'por' and lang != 'spa':
        LANGUAGE_PAIRS.append(('por', lang))

def get_pair_name(lang1: str, lang2: str) -> str:
    """Generate consistent pair name (alphabetical order)."""
    if lang1 < lang2:
        return f"{lang1}_{lang2}"
    else:
        return f"{lang2}_{lang1}"

def generate_task_yaml(lang1: str, lang2: str) -> str:
    """Generate YAML content for a bidirectional language pair task."""
    pair_name = get_pair_name(lang1, lang2)
    
    # Language display names
    lang_names = {
        'spa': 'Spanish',
        'por': 'Portuguese',
        'eng': 'English',
        'fra': 'French',
        'ita': 'Italian',
        'deu': 'German',
        'hin': 'Hindi',
        'cmn': 'Chinese',
        'arb': 'Arabic',
    }
    
    lang1_name = lang_names[lang1]
    lang2_name = lang_names[lang2]
    
    return f"""# Bidirectional {lang1_name} ↔ {lang2_name} translation task
task: flores_{pair_name}
task_alias: {lang1}↔{lang2}
custom_dataset: !function utils.load_{pair_name}
output_type: generate_until

# Splits
training_split: dev
validation_split: dev
test_split: devtest
fewshot_split: dev

# Prompting
doc_to_text: !function utils.doc_to_text
doc_to_target: !function utils.doc_to_target

# Generation settings
generation_kwargs:
  until:
    - "<|endoftext|>"
    - "</s>"
    - "\\n\\nTranslate"
    - "\\n\\n"
    - "Translation:"
  do_sample: false
  temperature: 0.0
  max_gen_toks: 250

# Filtering
filter_list:
  - name: "clean_translation"
    filter:
      - function: "regex"
        regex_pattern: "(.+?)(?:\\\\n|$)"
      - function: "take_first"

# Metrics - chrF and BLEU for comprehensive evaluation
metric_list:
  - metric: chrf
    aggregation: chrf
    higher_is_better: true
  - metric: bleu
    aggregation: bleu
    higher_is_better: true

# Performance optimizations
metadata:
  version: 3.0
  bootstrap_iters: 0  # Disable bootstrapping for maximum speed
  description: "Bidirectional {lang1_name}-{lang2_name} translation task"
"""

def main():
    """Generate all task YAML files."""
    base_dir = Path(__file__).parent
    
    print(f"Generating {len(LANGUAGE_PAIRS)} bidirectional task YAML files...")
    
    for lang1, lang2 in LANGUAGE_PAIRS:
        pair_name = get_pair_name(lang1, lang2)
        yaml_content = generate_task_yaml(lang1, lang2)
        
        output_path = base_dir / f"flores_{pair_name}.yaml"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"Generated: flores_{pair_name}.yaml")
    
    print(f"\n✅ Generated {len(LANGUAGE_PAIRS)} task files!")
    print("📁 Files are ready for use with lm-eval")

if __name__ == "__main__":
    main()
