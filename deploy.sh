#!/bin/bash
# Deployment script for lm-evaluation-harness
# This script handles the dependency conflicts in the project's optional dependencies

set -e

echo "🚀 Deploying lm-evaluation-harness..."

# Check if we're in a uv environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Error: Not in a virtual environment. Please activate your uv environment first."
    echo "   Run: source .venv/bin/activate"
    exit 1
fi

echo "📦 Installing core dependencies..."
# Install the project in editable mode with core dependencies only
# This bypasses the conflicting optional dependencies (acpbench vs math)
uv pip install -e .

echo "✅ Deployment complete!"
echo ""
echo "📋 Available commands:"
echo "   lm-eval --help                    # Show available tasks"
echo "   lm-eval --tasks list              # List all available tasks"
echo ""
echo "🔧 To install additional optional dependencies:"
echo "   uv pip install <package-name>     # Install specific packages"
echo "   uv sync --extra <optional-dep>    # Install optional dependency groups (if no conflicts)"
echo ""
echo "⚠️  Note: Some optional dependencies (acpbench, math) have conflicts."
echo "   Use 'uv pip install' for individual packages when needed."
