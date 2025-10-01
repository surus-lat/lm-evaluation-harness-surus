#!/usr/bin/env python3
"""
Build optimized FLORES+ dataset for LATAM translation tasks.

This script downloads FLORES+ once and creates a single optimized dataset
with all language pairs in the exact format needed for evaluation.

Usage:
    python build_dataset.py
"""

import json
import os
from pathlib import Path
import datasets
from typing import Dict, List


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

# Define all language pairs (bidirectional)
LANGUAGE_PAIRS = []

# All languages <-> Spanish
for lang in LANGUAGES.keys():
    if lang != 'spa_Latn':
        LANGUAGE_PAIRS.append(('spa_Latn', lang))
        LANGUAGE_PAIRS.append((lang, 'spa_Latn'))

# All languages <-> Portuguese  
for lang in LANGUAGES.keys():
    if lang != 'por_Latn':
        LANGUAGE_PAIRS.append(('por_Latn', lang))
        LANGUAGE_PAIRS.append((lang, 'por_Latn'))

# Remove duplicates
LANGUAGE_PAIRS = list(set(LANGUAGE_PAIRS))

print(f"Building dataset for {len(LANGUAGE_PAIRS)} language pairs...")


def load_flores_dataset():
    """Load the full FLORES+ dataset."""
    print("Loading FLORES+ dataset...")
    return datasets.load_dataset('openlanguagedata/flores_plus')


def build_optimized_dataset(full_dataset: datasets.DatasetDict, split: str) -> List[Dict]:
    """
    Build optimized dataset with all language pairs in simple format.
    
    Args:
        full_dataset: The full FLORES+ dataset
        split: Dataset split ('dev' or 'devtest')
    
    Returns:
        List of translation documents in optimized format
    """
    print(f"Building {split} split...")
    
    # Create language lookups
    language_data = {}
    for lang_code in LANGUAGES.keys():
        iso_code = lang_code.split('_')[0]
        lang_split = full_dataset[split].filter(lambda x: x['iso_639_3'] == iso_code)
        language_data[lang_code] = {doc['id']: doc for doc in lang_split}
        print(f"  Loaded {len(language_data[lang_code])} documents for {LANGUAGES[lang_code]} (ISO: {iso_code})")
        
        # Debug: Print first few IDs to check alignment
        if language_data[lang_code]:
            first_ids = sorted(list(language_data[lang_code].keys()), key=int)[:3]
            print(f"    First IDs: {first_ids}")
    
    # Build translation pairs
    translation_docs = []
    doc_id = 0
    
    for src_lang, tgt_lang in LANGUAGE_PAIRS:
        src_data = language_data[src_lang]
        tgt_data = language_data[tgt_lang]
        
        # Find common document IDs and ensure they match by FLORES ID, not just existence
        common_ids = set(src_data.keys()) & set(tgt_data.keys())
        
        # Sort by FLORES ID to ensure consistent ordering
        for flores_id in sorted(common_ids, key=int):
            src_doc = src_data[flores_id]
            tgt_doc = tgt_data[flores_id]
            
            # Validate that documents have the same FLORES ID
            if src_doc['id'] != tgt_doc['id']:
                print(f"WARNING: ID mismatch for {flores_id}: src={src_doc['id']}, tgt={tgt_doc['id']}")
                continue
            
            translation_docs.append({
                "id": str(doc_id),
                "flores_id": flores_id,
                "source_language": LANGUAGES[src_lang],
                "source_text": src_doc['text'],
                "target_language": LANGUAGES[tgt_lang], 
                "target_text": tgt_doc['text'],
                "language_pair": f"{src_lang}-{tgt_lang}",
                "source_code": src_lang,
                "target_code": tgt_lang,
            })
            doc_id += 1
    
    print(f"  Built {len(translation_docs)} translation pairs")
    return translation_docs


def save_dataset(docs: List[Dict], output_path: str):
    """Save dataset as JSONL."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"Saved {len(docs)} documents to {output_path}")


def main():
    # Output directory
    output_dir = Path(__file__).parent / "data"
    
    # Load FLORES+ dataset
    full_dataset = load_flores_dataset()
    
    # Build datasets for each split
    sample_doc = None
    for split in ['dev', 'devtest']:
        docs = build_optimized_dataset(full_dataset, split)
        
        # Save sample from first split
        if sample_doc is None and docs:
            sample_doc = docs[0]
        
        output_path = output_dir / f"{split}.jsonl"
        save_dataset(docs, str(output_path))
    
    print(f"\n✅ Dataset building complete!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📊 Total language pairs: {len(LANGUAGE_PAIRS)}")
    
    # Print sample
    if sample_doc:
        print(f"\n📝 Sample document:")
        print(json.dumps(sample_doc, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
