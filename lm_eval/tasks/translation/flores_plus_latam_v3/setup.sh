#!/bin/bash
# Setup script for FLORES+ LATAM v3 bidirectional language pair tasks

echo "🚀 Setting up FLORES+ LATAM v3 bidirectional language pair tasks..."
echo ""

# Check if we're in the right directory
if [[ ! -f "build_dataset.py" ]]; then
    echo "❌ Error: Please run this script from the flores_plus_latam_v3 directory"
    echo "   cd /path/to/lm-evaluation-harness/lm_eval/tasks/translation/flores_plus_latam_v3"
    exit 1
fi

# Build the datasets
echo "📊 Building bidirectional language pair datasets..."
python build_dataset.py

# Check if datasets were built successfully
if [[ -d "data" ]]; then
    echo ""
    echo "📊 Generating individual task YAML files..."
    python generate_tasks.py
    
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "📁 Created:"
    echo "   - $(find data -name '*.jsonl' | wc -l) dataset files"
    echo "   - $(ls flores_*.yaml 2>/dev/null | wc -l) individual task files"
    echo "   - 1 aggregate benchmark file (flores_plus_bidirectional.yaml)"
    echo ""
    echo "🧪 Test individual language pairs:"
    echo "   lm_eval --tasks flores_eng_spa --model your_model --limit 10"
    echo "   lm_eval --tasks flores_por_spa --model your_model --limit 10"
    echo ""
    echo "🚀 Run aggregate benchmark:"
    echo "   lm_eval --tasks flores_plus_bidirectional --model your_model"
    echo ""
    echo "🎯 Perfect middle ground: individual pairs + aggregate benchmark!"
else
    echo ""
    echo "❌ Dataset building failed. Check the error messages above."
    exit 1
fi
