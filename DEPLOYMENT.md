# Deployment Guide

This project has dependency conflicts between some optional dependencies that prevent normal `uv sync` from working. This guide explains how to properly deploy the project.

## The Problem

The project has conflicting dependencies:
- `acpbench` requires `antlr4-python3-runtime==4.7.2`
- `math` requires `antlr4-python3-runtime==4.11`
- Both are included in the `tasks` optional dependency group

This makes `uv sync` fail with "No solution found when resolving dependencies".

## The Solution

Use `uv pip install -e .` instead of `uv sync` to install the project with only its core dependencies, bypassing the conflicting optional dependencies.

## Quick Deployment

```bash
# 1. Activate your uv virtual environment
source .venv/bin/activate

# 2. Run the deployment script
./deploy.sh
```

## Manual Deployment

```bash
# 1. Activate your uv virtual environment
source .venv/bin/activate

# 2. Install the project in editable mode
uv pip install -e .

# 3. Install additional packages as needed
uv pip install <package-name>
```

## Installing Optional Dependencies

### Core Dependencies (Always Installed)
These are installed automatically with the project:
- `sentence-transformers`
- `wandb`
- `torch`
- `transformers`
- And all other core dependencies listed in `pyproject.toml`

### Optional Dependencies
Install these individually as needed:

```bash
# Individual packages
uv pip install sympy                    # For math tasks
uv pip install lark                     # For acpbench tasks
uv pip install pandas numpy             # For data processing

# Or use the optional dependency groups (if no conflicts)
uv sync --extra wandb                   # For wandb integration
uv sync --extra api                     # For API functionality
```

### Conflicting Dependencies
These cannot be installed together:
- `acpbench` (requires antlr4-python3-runtime==4.7.2)
- `math` (requires antlr4-python3-runtime==4.11)

Choose one or the other, or install packages individually.

## Verification

After deployment, verify everything works:

```bash
# Check if lm-eval is available
lm-eval --help

# List available tasks
lm-eval --tasks list

# Check installed packages
uv pip list | grep -E "(sentence-transformers|wandb|torch)"
```

## Troubleshooting

### "No solution found when resolving dependencies"
- Use `uv pip install -e .` instead of `uv sync`
- Install optional dependencies individually with `uv pip install`

### "Package not found" errors
- Make sure you're in the correct virtual environment
- Run `uv pip install <package-name>` to install missing packages

### "Command not found: lm-eval"
- Make sure the project is installed in editable mode: `uv pip install -e .`
- Check that your virtual environment is activated
