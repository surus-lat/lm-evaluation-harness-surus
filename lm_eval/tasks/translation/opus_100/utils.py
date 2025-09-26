"""
Utility functions for OPUS-100 translation tasks.
"""

import datasets
from typing import Dict, Any, Callable


def process_docs_en_es(dataset: datasets.Dataset) -> datasets.Dataset:
    """
    Process OPUS-100 en-es dataset for translation tasks.
    
    This function processes the dataset to extract English-Spanish translation pairs
    from the OPUS-100 format.
    """
    def _process_doc(doc):
        translation = doc['translation']
        return {
            'src_text': translation['en'],
            'tgt_text': translation['es'],
        }
    
    return dataset.map(_process_doc)


def process_docs_en_pt(dataset: datasets.Dataset) -> datasets.Dataset:
    """
    Process OPUS-100 en-pt dataset for translation tasks.
    
    This function processes the dataset to extract English-Portuguese translation pairs
    from the OPUS-100 format.
    """
    def _process_doc(doc):
        translation = doc['translation']
        return {
            'src_text': translation['en'],
            'tgt_text': translation['pt'],
        }
    
    return dataset.map(_process_doc)


def doc_to_text_en_es(doc):
    """Generate the input prompt for English to Spanish translation."""
    return f"Translate the following sentence from English to Spanish:\n\n{doc['src_text']}\n\nSpanish translation: "


def doc_to_text_en_pt(doc):
    """Generate the input prompt for English to Portuguese translation.""" 
    return f"Translate the following sentence from English to Portuguese:\n\n{doc['src_text']}\n\nPortuguese translation: "


def doc_to_target(doc):
    """Generate the target template."""
    return doc['tgt_text']
