#!/usr/bin/env python3
"""
Build optimized FLORES+ dataset for bidirectional language pair tasks (v3).

This script creates separate datasets for each bidirectional language pair
(e.g., Spanish-English covers both spa->eng and eng->spa).

Usage:
    python build_dataset.py
"""

import json
import os
from pathlib import Path
import datasets
from typing import Dict, List, Tuple


# Language configurations
LANGUAGES = {
    'spa_Latn': 'Spanish',
    'por_Latn': 'Portuguese', 
    'eng_Latn': 'English',
    'fra_Latn': 'French',
    'ita_Latn': 'Italian',
    'deu_Latn': 'German',
    'hin_Deva': 'Hindi',
    'cmn_Hans': 'Chinese',
    'arb_Arab': 'Arabic',
}

# Define LATAM-focused bidirectional language pairs
# All languages <-> Spanish + All languages <-> Portuguese (excluding spa-spa and por-por)
LANGUAGE_PAIRS = []

# All languages <-> Spanish (excluding Spanish itself)
for lang_code in LANGUAGES.keys():
    if lang_code != 'spa_Latn':
        LANGUAGE_PAIRS.append(('spa_Latn', lang_code))

# All languages <-> Portuguese (excluding Portuguese itself and Spanish - already covered above)
for lang_code in LANGUAGES.keys():
    if lang_code != 'por_Latn' and lang_code != 'spa_Latn':
        LANGUAGE_PAIRS.append(('por_Latn', lang_code))

print(f"Building datasets for {len(LANGUAGE_PAIRS)} bidirectional language pairs...")


def load_flores_dataset():
    """Load the full FLORES+ dataset."""
    print("Loading FLORES+ dataset...")
    return datasets.load_dataset('openlanguagedata/flores_plus')


def build_bidirectional_pair_dataset(
    full_dataset: datasets.DatasetDict, 
    lang1: str, 
    lang2: str, 
    split: str
) -> List[Dict]:
    """
    Build bidirectional dataset for a specific language pair.
    
    Args:
        full_dataset: The full FLORES+ dataset
        lang1: First language code (e.g., 'spa_Latn')
        lang2: Second language code (e.g., 'eng_Latn')
        split: Dataset split ('dev' or 'devtest')
    
    Returns:
        List of translation documents for both directions
    """
    iso1 = lang1.split('_')[0]
    iso2 = lang2.split('_')[0]
    
    # Filter dataset for each language
    lang1_split = full_dataset[split].filter(lambda x: x['iso_639_3'] == iso1)
    lang2_split = full_dataset[split].filter(lambda x: x['iso_639_3'] == iso2)
    
    # Create lookup dictionaries
    lang1_lookup = {doc['id']: doc for doc in lang1_split}
    lang2_lookup = {doc['id']: doc for doc in lang2_split}
    
    # Find common document IDs
    common_ids = set(lang1_lookup.keys()) & set(lang2_lookup.keys())
    
    # Build bidirectional translation pairs
    translation_docs = []
    doc_id = 0
    
    for flores_id in sorted(common_ids, key=int):
        lang1_doc = lang1_lookup[flores_id]
        lang2_doc = lang2_lookup[flores_id]
        
        # Validate that documents have the same FLORES ID
        if lang1_doc['id'] != lang2_doc['id']:
            print(f"WARNING: ID mismatch for {flores_id}: {lang1_doc['id']} != {lang2_doc['id']}")
            continue
        
        # Direction 1: lang1 -> lang2
        translation_docs.append({
            "id": str(doc_id),
            "flores_id": flores_id,
            "source_language": LANGUAGES[lang1],
            "source_text": lang1_doc['text'],
            "target_language": LANGUAGES[lang2],
            "target_text": lang2_doc['text'],
            "language_pair": f"{lang1}-{lang2}",
            "direction": f"{lang1}->{lang2}",
            "source_code": lang1,
            "target_code": lang2,
        })
        doc_id += 1
        
        # Direction 2: lang2 -> lang1
        translation_docs.append({
            "id": str(doc_id),
            "flores_id": flores_id,
            "source_language": LANGUAGES[lang2],
            "source_text": lang2_doc['text'],
            "target_language": LANGUAGES[lang1],
            "target_text": lang1_doc['text'],
            "language_pair": f"{lang1}-{lang2}",  # Keep consistent pair naming
            "direction": f"{lang2}->{lang1}",
            "source_code": lang2,
            "target_code": lang1,
        })
        doc_id += 1
    
    return translation_docs


def save_dataset(docs: List[Dict], output_path: str):
    """Save dataset as JSONL."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"Saved {len(docs)} documents to {output_path}")


def get_pair_name(lang1: str, lang2: str) -> str:
    """Generate consistent pair name (alphabetical order)."""
    lang1_short = lang1.split('_')[0]
    lang2_short = lang2.split('_')[0]
    
    # Always put in alphabetical order for consistency
    if lang1_short < lang2_short:
        return f"{lang1_short}_{lang2_short}"
    else:
        return f"{lang2_short}_{lang1_short}"


def main():
    # Output directory
    output_dir = Path(__file__).parent / "data"
    
    # Load FLORES+ dataset
    full_dataset = load_flores_dataset()
    
    # Build datasets for each language pair and split
    for lang1, lang2 in LANGUAGE_PAIRS:
        pair_name = get_pair_name(lang1, lang2)
        print(f"\nProcessing {LANGUAGES[lang1]} ↔ {LANGUAGES[lang2]} ({pair_name})...")
        
        for split in ['dev', 'devtest']:
            docs = build_bidirectional_pair_dataset(full_dataset, lang1, lang2, split)
            
            output_path = output_dir / pair_name / f"{split}.jsonl"
            save_dataset(docs, str(output_path))
    
    print(f"\n✅ Dataset building complete!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📊 Total language pairs: {len(LANGUAGE_PAIRS)}")
    
    # Print sample from first pair
    first_pair = LANGUAGE_PAIRS[0]
    pair_name = get_pair_name(first_pair[0], first_pair[1])
    sample_file = output_dir / pair_name / "dev.jsonl"
    
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample = json.loads(f.readline().strip())
            print(f"\n📝 Sample document from {pair_name}:")
            print(json.dumps(sample, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
