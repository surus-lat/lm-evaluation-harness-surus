"""
Utilities for optimized FLORES+ translation task.
"""

import datasets
import json
import os
from pathlib import Path
from typing import Dict


def load_optimized_flores_dataset(**kwargs):
    """
    Load the optimized FLORES+ dataset from local JSONL files.
    
    Args:
        **kwargs: Additional arguments passed by lm-eval framework (ignored)
    
    Returns:
        Dictionary with split names as keys and datasets as values
    """
    data_dir = Path(__file__).parent / "data"
    
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
            print(f"Loaded {len(docs)} translation pairs for {split} split")
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
