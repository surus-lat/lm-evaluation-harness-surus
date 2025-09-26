# OPUS-100 Translation Tasks

This directory contains translation tasks based on the [OPUS-100](https://huggingface.co/datasets/Helsinki-NLP/opus-100) dataset from Helsinki-NLP.

## Tasks

### Individual Tasks

- **opus_100_en-es**: English to Spanish translation using the OPUS-100 en-es subset
- **opus_100_en-pt**: English to Portuguese translation using the OPUS-100 en-pt subset

### Group Task

- **opus**: Group containing both en-es and en-pt tasks with aggregated metrics

## Dataset Details

The OPUS-100 dataset is an English-centric multilingual corpus covering 100 languages. It contains approximately 55M sentence pairs with up to 1M training pairs per language pair.

For these tasks, we use:
- **Training split**: train
- **Validation split**: validation  
- **Test split**: test (used for evaluation)
- **Few-shot split**: train

## Metrics

All tasks evaluate using:
- **BLEU**: Bilingual Evaluation Understudy score
- **TER**: Translation Error Rate (lower is better)
- **chrF**: Character n-gram F-score

## Citation

If you use these tasks, please cite the OPUS-100 paper:

```bibtex
@inproceedings{zhang-etal-2020-improving,
    title = "Improving Massively Multilingual Neural Machine Translation and Zero-Shot Translation",
    author = "Zhang, Biao  and
      Williams, Philip  and
      Titov, Ivan  and
      Sennrich, Rico",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.148",
    pages = "1628--1639",
}
```
