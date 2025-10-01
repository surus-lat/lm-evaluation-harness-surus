"""
Utilities for bidirectional FLORES+ language pair tasks (v3).
"""

import datasets
import json
import os
from pathlib import Path
from typing import Dict


def load_bidirectional_pair_dataset(pair_name: str, **kwargs):
    """
    Load a bidirectional language pair dataset from local JSONL files.
    
    Args:
        pair_name: Language pair name (e.g., 'eng_spa', 'por_spa')
        **kwargs: Additional arguments passed by lm-eval framework (ignored)
    
    Returns:
        Dictionary with split names as keys and datasets as values
    """
    data_dir = Path(__file__).parent / "data" / pair_name
    
    datasets_dict = {}
    
    for split in ['dev', 'devtest']:
        file_path = data_dir / f"{split}.jsonl"
        
        if file_path.exists():
            # Load JSONL file
            docs = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    docs.append(json.loads(line.strip()))
            
            # Convert to HuggingFace dataset
            datasets_dict[split] = datasets.Dataset.from_list(docs)
            print(f"Loaded {len(docs)} translation pairs for {pair_name} {split} split")
        else:
            print(f"Warning: {file_path} not found. Run build_dataset.py first.")
            datasets_dict[split] = datasets.Dataset.from_list([])
    
    return datasets_dict


def doc_to_text(doc):
    """
    Generate translation prompt from document.
    
    Format: "Translate this sentence from {source_language} to {target_language}: {source_text}. Translation:"
    """
    return f"Translate this sentence from {doc['source_language']} to {doc['target_language']}: {doc['source_text']}. Translation:"


def doc_to_target(doc):
    """Generate target text."""
    return doc['target_text']


# Create specific dataset loading functions for each language pair
def load_arb_cmn(**kwargs):
    return load_bidirectional_pair_dataset('arb_cmn', **kwargs)

def load_arb_deu(**kwargs):
    return load_bidirectional_pair_dataset('arb_deu', **kwargs)

def load_arb_eng(**kwargs):
    return load_bidirectional_pair_dataset('arb_eng', **kwargs)

def load_arb_fra(**kwargs):
    return load_bidirectional_pair_dataset('arb_fra', **kwargs)

def load_arb_hin(**kwargs):
    return load_bidirectional_pair_dataset('arb_hin', **kwargs)

def load_arb_ita(**kwargs):
    return load_bidirectional_pair_dataset('arb_ita', **kwargs)

def load_arb_por(**kwargs):
    return load_bidirectional_pair_dataset('arb_por', **kwargs)

def load_arb_spa(**kwargs):
    return load_bidirectional_pair_dataset('arb_spa', **kwargs)

def load_cmn_deu(**kwargs):
    return load_bidirectional_pair_dataset('cmn_deu', **kwargs)

def load_cmn_eng(**kwargs):
    return load_bidirectional_pair_dataset('cmn_eng', **kwargs)

def load_cmn_fra(**kwargs):
    return load_bidirectional_pair_dataset('cmn_fra', **kwargs)

def load_cmn_hin(**kwargs):
    return load_bidirectional_pair_dataset('cmn_hin', **kwargs)

def load_cmn_ita(**kwargs):
    return load_bidirectional_pair_dataset('cmn_ita', **kwargs)

def load_cmn_por(**kwargs):
    return load_bidirectional_pair_dataset('cmn_por', **kwargs)

def load_cmn_spa(**kwargs):
    return load_bidirectional_pair_dataset('cmn_spa', **kwargs)

def load_deu_eng(**kwargs):
    return load_bidirectional_pair_dataset('deu_eng', **kwargs)

def load_deu_fra(**kwargs):
    return load_bidirectional_pair_dataset('deu_fra', **kwargs)

def load_deu_hin(**kwargs):
    return load_bidirectional_pair_dataset('deu_hin', **kwargs)

def load_deu_ita(**kwargs):
    return load_bidirectional_pair_dataset('deu_ita', **kwargs)

def load_deu_por(**kwargs):
    return load_bidirectional_pair_dataset('deu_por', **kwargs)

def load_deu_spa(**kwargs):
    return load_bidirectional_pair_dataset('deu_spa', **kwargs)

def load_eng_fra(**kwargs):
    return load_bidirectional_pair_dataset('eng_fra', **kwargs)

def load_eng_hin(**kwargs):
    return load_bidirectional_pair_dataset('eng_hin', **kwargs)

def load_eng_ita(**kwargs):
    return load_bidirectional_pair_dataset('eng_ita', **kwargs)

def load_eng_por(**kwargs):
    return load_bidirectional_pair_dataset('eng_por', **kwargs)

def load_eng_spa(**kwargs):
    return load_bidirectional_pair_dataset('eng_spa', **kwargs)

def load_fra_hin(**kwargs):
    return load_bidirectional_pair_dataset('fra_hin', **kwargs)

def load_fra_ita(**kwargs):
    return load_bidirectional_pair_dataset('fra_ita', **kwargs)

def load_fra_por(**kwargs):
    return load_bidirectional_pair_dataset('fra_por', **kwargs)

def load_fra_spa(**kwargs):
    return load_bidirectional_pair_dataset('fra_spa', **kwargs)

def load_hin_ita(**kwargs):
    return load_bidirectional_pair_dataset('hin_ita', **kwargs)

def load_hin_por(**kwargs):
    return load_bidirectional_pair_dataset('hin_por', **kwargs)

def load_hin_spa(**kwargs):
    return load_bidirectional_pair_dataset('hin_spa', **kwargs)

def load_ita_por(**kwargs):
    return load_bidirectional_pair_dataset('ita_por', **kwargs)

def load_ita_spa(**kwargs):
    return load_bidirectional_pair_dataset('ita_spa', **kwargs)

def load_por_spa(**kwargs):
    return load_bidirectional_pair_dataset('por_spa', **kwargs)
