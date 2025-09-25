"""
Utility functions for FLORES+ LATAM translation tasks.
"""

import datasets
from typing import Dict, Any, Callable
import os
import re


# Global cache for the full FLORES+ dataset
_full_dataset_cache = None

def get_full_flores_dataset():
    """Get the full FLORES+ dataset, using cache if available."""
    global _full_dataset_cache
    if _full_dataset_cache is None:
        print("Loading full FLORES+ dataset (this will be cached for subsequent tasks)...")
        _full_dataset_cache = datasets.load_dataset('openlanguagedata/flores_plus')
    return _full_dataset_cache

def create_process_docs_function(target_language: str) -> Callable:
    """
    Create a process_docs function for a specific target language.
    
    Args:
        target_language: The target language code (e.g., 'por', 'spa', 'eng')
    
    Returns:
        A process_docs function configured for the target language
    """
    def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
        """
        Process FLORES+ dataset for translation tasks.
        
        This function takes a dataset that has already been loaded by the framework
        and processes it to create source-target pairs for translation.
        """
        # Map language codes to ISO 639-3 codes
        lang_to_iso = {
            'spa': 'spa',
            'por': 'por', 
            'eng': 'eng',
            'fra': 'fra',
            'ita': 'ita',
            'deu': 'deu',
            'cat': 'cat',
            'eus': 'eus',
            'glg': 'glg',
        }
        
        # Get the target language ISO code
        tgt_iso = lang_to_iso.get(target_language, 'por')
        
        # Get the full dataset (cached)
        full_dataset = get_full_flores_dataset()
        
        # Get the current split name from the dataset
        current_split = list(dataset.keys())[0] if hasattr(dataset, 'keys') else 'dev'
        
        # Filter the full dataset to get only target language documents
        tgt_split = full_dataset[current_split].filter(lambda x: x['iso_639_3'] == tgt_iso)
        
        # Create a lookup dictionary for faster matching
        tgt_lookup = {doc['id']: doc for doc in tgt_split}
        
        # Process the dataset to create pairs
        def _process_doc(doc):
            # Find the corresponding target document by ID
            tgt_doc = tgt_lookup.get(doc['id'])
            
            if tgt_doc is None:
                # If no matching target found, skip this document
                return None
                
            return {
                'id': doc['id'],
                'src_text': doc['text'],
                'tgt_text': tgt_doc['text'],
            }
        
        # Apply the processing function and filter out None values
        processed_docs = []
        for doc in dataset:
            processed_doc = _process_doc(doc)
            if processed_doc is not None:
                processed_docs.append(processed_doc)
        
        return datasets.Dataset.from_list(processed_docs)
    
    return process_docs


# Create specific process_docs functions for all language pairs
process_docs_spa_to_por = create_process_docs_function('por')
process_docs_por_to_spa = create_process_docs_function('spa')
process_docs_spa_to_eng = create_process_docs_function('eng')
process_docs_eng_to_spa = create_process_docs_function('spa')
process_docs_por_to_eng = create_process_docs_function('eng')
process_docs_eng_to_por = create_process_docs_function('por')

# Additional language pairs
process_docs_spa_to_fra = create_process_docs_function('fra')
process_docs_fra_to_spa = create_process_docs_function('spa')
process_docs_spa_to_ita = create_process_docs_function('ita')
process_docs_ita_to_spa = create_process_docs_function('spa')
process_docs_spa_to_deu = create_process_docs_function('deu')
process_docs_deu_to_spa = create_process_docs_function('spa')
process_docs_spa_to_cat = create_process_docs_function('cat')
process_docs_cat_to_spa = create_process_docs_function('spa')
process_docs_spa_to_eus = create_process_docs_function('eus')
process_docs_eus_to_spa = create_process_docs_function('spa')
process_docs_spa_to_glg = create_process_docs_function('glg')
process_docs_glg_to_spa = create_process_docs_function('spa')

process_docs_por_to_fra = create_process_docs_function('fra')
process_docs_fra_to_por = create_process_docs_function('por')
process_docs_por_to_ita = create_process_docs_function('ita')
process_docs_ita_to_por = create_process_docs_function('por')
process_docs_por_to_deu = create_process_docs_function('deu')
process_docs_deu_to_por = create_process_docs_function('por')
process_docs_por_to_cat = create_process_docs_function('cat')
process_docs_cat_to_por = create_process_docs_function('por')
process_docs_por_to_eus = create_process_docs_function('eus')
process_docs_eus_to_por = create_process_docs_function('por')
process_docs_por_to_glg = create_process_docs_function('glg')
process_docs_glg_to_por = create_process_docs_function('por')

# Default process_docs function (Spanish to Portuguese)
def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Default process_docs function for Spanish to Portuguese translation."""
    return process_docs_spa_to_por(dataset)


def doc_to_text(doc):
    """Generate the input prompt template."""
    # This is a generic function that works for any language pair
    # The actual language names will be determined by the dataset_name in the YAML
    return f"Source sentence: {doc['src_text']}\nTarget sentence:"


def doc_to_target(doc):
    """Generate the target template."""
    return doc['tgt_text']