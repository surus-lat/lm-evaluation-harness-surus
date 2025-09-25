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
        # The dataset passed to us is already from a specific split, so we need to 
        # determine which split it came from by looking at the dataset length
        if len(dataset) == 997:
            current_split = 'dev'
        elif len(dataset) == 1012:
            current_split = 'devtest'
        else:
            # Fallback to dev if we can't determine
            current_split = 'dev'
        
        
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


def create_doc_to_text_function(src_lang: str, tgt_lang: str) -> Callable:
    """Create a doc_to_text function for a specific language pair."""
    lang_names = {
        'spa': 'Spanish',
        'por': 'Portuguese', 
        'eng': 'English',
        'fra': 'French',
        'ita': 'Italian',
        'deu': 'German',
        'cat': 'Catalan',
        'eus': 'Basque',
        'glg': 'Galician',
    }
    
    src_name = lang_names.get(src_lang, src_lang)
    tgt_name = lang_names.get(tgt_lang, tgt_lang)
    
    def doc_to_text(doc):
        return f"Translate the following sentence from {src_name} to {tgt_name}:\n\n{doc['src_text']}\n\n{tgt_name} translation:"
    
    return doc_to_text

def doc_to_target(doc):
    """Generate the target template."""
    return doc['tgt_text']

# Create specific doc_to_text functions for common language pairs
doc_to_text_eng_to_spa = create_doc_to_text_function('eng', 'spa')
doc_to_text_spa_to_eng = create_doc_to_text_function('spa', 'eng')
doc_to_text_spa_to_por = create_doc_to_text_function('spa', 'por')
doc_to_text_por_to_spa = create_doc_to_text_function('por', 'spa')
doc_to_text_eng_to_por = create_doc_to_text_function('eng', 'por')
doc_to_text_por_to_eng = create_doc_to_text_function('por', 'eng')

# Additional language pairs
doc_to_text_spa_to_fra = create_doc_to_text_function('spa', 'fra')
doc_to_text_fra_to_spa = create_doc_to_text_function('fra', 'spa')
doc_to_text_spa_to_ita = create_doc_to_text_function('spa', 'ita')
doc_to_text_ita_to_spa = create_doc_to_text_function('ita', 'spa')
doc_to_text_spa_to_deu = create_doc_to_text_function('spa', 'deu')
doc_to_text_deu_to_spa = create_doc_to_text_function('deu', 'spa')
doc_to_text_spa_to_cat = create_doc_to_text_function('spa', 'cat')
doc_to_text_cat_to_spa = create_doc_to_text_function('cat', 'spa')
doc_to_text_spa_to_eus = create_doc_to_text_function('spa', 'eus')
doc_to_text_eus_to_spa = create_doc_to_text_function('eus', 'spa')
doc_to_text_spa_to_glg = create_doc_to_text_function('spa', 'glg')
doc_to_text_glg_to_spa = create_doc_to_text_function('glg', 'spa')

doc_to_text_por_to_fra = create_doc_to_text_function('por', 'fra')
doc_to_text_fra_to_por = create_doc_to_text_function('fra', 'por')
doc_to_text_por_to_ita = create_doc_to_text_function('por', 'ita')
doc_to_text_ita_to_por = create_doc_to_text_function('ita', 'por')
doc_to_text_por_to_deu = create_doc_to_text_function('por', 'deu')
doc_to_text_deu_to_por = create_doc_to_text_function('deu', 'por')
doc_to_text_por_to_cat = create_doc_to_text_function('por', 'cat')
doc_to_text_cat_to_por = create_doc_to_text_function('cat', 'por')
doc_to_text_por_to_eus = create_doc_to_text_function('por', 'eus')
doc_to_text_eus_to_por = create_doc_to_text_function('eus', 'por')
doc_to_text_por_to_glg = create_doc_to_text_function('por', 'glg')
doc_to_text_glg_to_por = create_doc_to_text_function('glg', 'por')

# Default function (English to Spanish)
def doc_to_text(doc):
    """Default doc_to_text function for English to Spanish translation."""
    return doc_to_text_eng_to_spa(doc)