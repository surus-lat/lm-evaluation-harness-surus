# FLORES+ LATAM v2 - Optimized Translation Tasks

This is the **optimized version** of FLORES+ translation tasks, designed for maximum performance with all LATAM language pairs in a single task.

## 🚀 Quick Start

### 1. Build the Dataset (One-time setup)
```bash
cd /home/mauro/dev/benchy/external/lm-evaluation-harness/lm_eval/tasks/translation/flores_plus_latam_v2
python build_dataset.py
```

### 2. Test the Task
```bash
# Test with limited samples
lm_eval --tasks flores_plus_optimized --model your_model --limit 10

# Full evaluation
lm_eval --tasks flores_plus_optimized --model your_model
```

## 📊 What This Gives You

### Performance Improvements
- **32 tasks → 1 task**: Massive reduction in task overhead
- **No runtime dataset processing**: Pre-built, optimized format
- **No bootstrapping**: Disabled for maximum speed
- **Local data**: No HuggingFace downloads during evaluation

### Language Coverage
All LATAM language pairs:
- Spanish ↔ Portuguese, English, French, Italian, German, Hindi, Chinese, Arabic
- Portuguese ↔ Spanish, English, French, Italian, German, Hindi, Chinese, Arabic

### Data Format
Each document has this simple, clean format:
```json
{
  "id": "26",
  "source_language": "Spanish",
  "source_text": "Hola mundo",
  "target_language": "English", 
  "target_text": "Hello world",
  "language_pair": "spa_Latn-eng_Latn"
}
```

### Prompt Format
Super simple prompting:
```
Translate this sentence from Spanish to English: Hola mundo. Translation:
```

## 📁 Files

- `build_dataset.py` - One-time dataset builder
- `utils.py` - Simple task utilities
- `flores_plus_optimized.yaml` - Main task configuration
- `data/dev.jsonl` - Development split (generated)
- `data/devtest.jsonl` - Test split (generated)

## 🎯 Design Philosophy

**Move complexity to dataset building, keep task config dead simple.**

- ✅ Complex dataset processing happens once during build
- ✅ Task configuration is minimal and clean
- ✅ Runtime evaluation is blazing fast
- ✅ All language pairs in one unified task

## 🔧 Customization

### Add/Remove Languages
Edit `LANGUAGES` dict in `build_dataset.py`:
```python
LANGUAGES = {
    'spa_Latn': 'Spanish',
    'por_Latn': 'Portuguese',
    # Add more languages here
}
```

### Change Prompt Format
Edit `doc_to_text()` in `utils.py`:
```python
def doc_to_text(doc):
    return f"Translate from {doc['source_language']} to {doc['target_language']}: {doc['source_text']}. Translation:"
```

## 📈 Expected Performance

- **10-20x faster** than individual task approach
- **Single bootstrapping calculation** (if enabled)
- **Unified metrics** across all language pairs
- **Minimal memory footprint** with pre-processed data

## 🎯 Usage in Your Pipeline

Replace your translation task list:
```yaml
# Old
tasks:
  - "translation"  # 32+ individual tasks

# New  
tasks:
  - "flores_plus_optimized"  # 1 optimized task
```

That's it! 🚀
