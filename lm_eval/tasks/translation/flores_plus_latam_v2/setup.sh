#!/bin/bash
# Setup script for FLORES+ LATAM v2 optimized translation tasks

echo "🚀 Setting up FLORES+ LATAM v2 optimized translation tasks..."
echo ""

# Check if we're in the right directory
if [[ ! -f "build_dataset.py" ]]; then
    echo "❌ Error: Please run this script from the flores_plus_latam_v2 directory"
    echo "   cd /path/to/lm-evaluation-harness/lm_eval/tasks/translation/flores_plus_latam_v2"
    exit 1
fi

# Build the dataset
echo "📊 Building optimized FLORES+ dataset..."
python build_dataset.py

# Check if dataset was built successfully
if [[ -f "data/dev.jsonl" && -f "data/devtest.jsonl" ]]; then
    echo ""
    echo "✅ Dataset built successfully!"
    echo ""
    echo "📁 Files created:"
    echo "   - data/dev.jsonl ($(wc -l < data/dev.jsonl) translation pairs)"
    echo "   - data/devtest.jsonl ($(wc -l < data/devtest.jsonl) translation pairs)"
    echo ""
    echo "🧪 Test the task with:"
    echo "   lm_eval --tasks flores_plus_optimized --model your_model --limit 10"
    echo ""
    echo "🚀 Run full evaluation with:"
    echo "   lm_eval --tasks flores_plus_optimized --model your_model"
    echo ""
    echo "🎯 Ready to use! This single task replaces 32+ individual FLORES+ tasks."
else
    echo ""
    echo "❌ Dataset building failed. Check the error messages above."
    exit 1
fi
