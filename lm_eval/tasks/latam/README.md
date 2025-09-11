# LATAM

### Tasks

## Spanish

- aquas
- belebele_spa_Latn
- clindiagnoses
- clintreates
- copa_es
- crows_pairs_spanish
- escola
- fake_news_es
- humorqa
- mgsm_direct_es_spanish_bench
- noticia
- offendes
- openbookqa_es
- paws_es_spanish_bench
- ragquas
- spalawex
- teleia
- wnli_es
- xnli_es_spanish_bench
- xlsum_es
- xquad_es
- xstorycloze_es

### Reproducibility

To evaluate a model on this benchmark run:

```bash
lm_eval --model --model=hf \
    --model_args "pretrained=<your_model>,use_accelerate=True,revision=<your_model_revision>" \
    --tasks laleaderboard \
    --num_fewshot 5 \
    --batch_size 1
```
