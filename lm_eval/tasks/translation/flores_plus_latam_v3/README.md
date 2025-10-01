# FLORES+ LATAM v3 - Bidirectional Language Pair Tasks

This is the **v3 implementation** that provides the perfect middle ground: **individual bidirectional language pair tasks** + **aggregate benchmark**.

## 🎯 What You Get

### **Individual Bidirectional Tasks**
- `flores_eng_spa` - English ↔ Spanish (both directions in one task)
- `flores_por_spa` - Portuguese ↔ Spanish (both directions in one task)
- `flores_eng_por` - English ↔ Portuguese (both directions in one task)
- ... and 21 more language pairs

### **Aggregate Benchmark**
- `flores_plus_bidirectional` - All language pairs combined

## 🚀 Quick Start

### 1. Setup (One-time)
```bash
cd /home/mauro/dev/benchy/external/lm-evaluation-harness/lm_eval/tasks/translation/flores_plus_latam_v3
./setup.sh
```

### 2. Test Individual Language Pairs
```bash
# Test Spanish-English bidirectional
lm_eval --tasks flores_eng_spa --model your_model --limit 10

# Test Portuguese-Spanish bidirectional  
lm_eval --tasks flores_por_spa --model your_model --limit 10
```

### 3. Run Aggregate Benchmark
```bash
# All language pairs in one benchmark
lm_eval --tasks flores_plus_bidirectional --model your_model
```

## 📊 Architecture

### **Data Structure**
Each bidirectional task contains documents for both directions:
```json
{
  "id": "0",
  "source_language": "Spanish",
  "source_text": "Hola mundo",
  "target_language": "English",
  "target_text": "Hello world",
  "direction": "spa_Latn->eng_Latn"
}
```

### **Task Organization**
```
flores_plus_latam_v3/
├── data/
│   ├── eng_spa/
│   │   ├── dev.jsonl      # English↔Spanish pairs
│   │   └── devtest.jsonl
│   ├── por_spa/
│   │   ├── dev.jsonl      # Portuguese↔Spanish pairs
│   │   └── devtest.jsonl
│   └── ... (24 total pairs)
├── flores_eng_spa.yaml    # Individual task configs
├── flores_por_spa.yaml
├── ... (24 total tasks)
└── flores_plus_bidirectional.yaml  # Aggregate benchmark
```

## 🎯 Perfect Middle Ground

| Approach | Tasks | Granularity | Speed | Use Case |
|----------|-------|-------------|-------|----------|
| **v1 (Original)** | 32+ individual | Per direction | Slow | Detailed analysis |
| **v2 (Unified)** | 1 mega-task | All combined | Fast | Quick benchmarking |
| **v3 (This)** | 24 bidirectional | Per language pair | Fast | **Perfect balance** |

## 🚀 Benefits

### ✅ **Individual Language Pair Analysis**
- Track performance per language pair
- Debug specific translation directions
- Compare related languages (Spanish vs Portuguese)

### ✅ **Aggregate Benchmarking**
- Single score for overall translation capability
- Easy model comparison
- Clean leaderboard reporting

### ✅ **Maximum Speed**
- Local preprocessing (no runtime dataset loading)
- chrF-only metric (fast computation)
- No bootstrapping (instant results)
- Bidirectional tasks (2× fewer tasks than v1)

### ✅ **Flexible Usage**
```bash
# Focus on core LATAM pairs
lm_eval --tasks flores_eng_spa,flores_por_spa,flores_eng_por

# Test all Spanish pairs
lm_eval --tasks flores_arb_spa,flores_cmn_spa,flores_deu_spa,flores_eng_spa,flores_fra_spa,flores_hin_spa,flores_ita_spa,flores_por_spa

# Full benchmark
lm_eval --tasks flores_plus_bidirectional
```

## 📈 Expected Performance

- **Individual tasks**: ~2-3 minutes each
- **Aggregate benchmark**: ~45-60 minutes total
- **No bootstrapping delays**: Instant metric computation
- **Clean output**: One chrF score per task

## 🎯 Language Coverage

**24 bidirectional language pairs** covering:
- **LATAM focus**: Spanish ↔ Portuguese, English
- **European**: French, Italian, German
- **Global**: Hindi, Chinese, Arabic
- **All combinations**: Every language paired with every other language

This gives you the **perfect balance** of granular analysis and aggregate benchmarking! 🎉
