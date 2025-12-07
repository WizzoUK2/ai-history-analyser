# AI History Analyser

[![CI](https://github.com/WizzoUK2/ai-history-analyser/actions/workflows/ci.yml/badge.svg)](https://github.com/WizzoUK2/ai-history-analyser/actions/workflows/ci.yml)

A tool to analyze chat histories from ChatGPT, Claude, Gemini, and other AI assistants to identify unfinished projects, prioritize them, and optionally export to Obsidian.

## Features

- **Multi-Platform Support**: Import chat histories from ChatGPT, Claude, Gemini, and extensible for others
- **Unfinished Project Detection**: Automatically identifies incomplete tasks and projects
- **Prioritization**: Ranks unfinished projects based on various criteria
- **Obsidian Integration**: Export results to Obsidian markdown format
- **Extensible**: Easy to add new analysis types and platforms

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Export your chat history** from ChatGPT, Claude, or Gemini (usually available in account settings)

3. **Run analysis:**
   ```bash
   python -m ai_history_analyser analyze --input chatgpt_export.json --platform chatgpt
   ```

4. **Export to Obsidian:**
   ```bash
   python -m ai_history_analyser analyze \
     --input chatgpt.json --platform chatgpt \
     --obsidian --obsidian-path ~/Documents/ObsidianVault
   ```

## Usage

### Basic Analysis

```bash
python -m ai_history_analyser analyze --input path/to/chatgpt_export.json --platform chatgpt
```

### Multiple Platforms

```bash
python -m ai_history_analyser analyze \
  --input chatgpt.json --platform chatgpt \
  --input claude.json --platform claude \
  --input gemini.json --platform gemini
```

### Export to Obsidian

```bash
python -m ai_history_analyser analyze \
  --input chatgpt.json --platform chatgpt \
  --obsidian --obsidian-path /path/to/obsidian/vault
```

### List Unfinished Projects

```bash
python -m ai_history_analyser list-unfinished --input chatgpt.json --platform chatgpt
```

### Create Configuration File

```bash
python -m ai_history_analyser init-config
```

## Project Structure

```
ai_history_analyser/
├── parsers/          # Platform-specific history parsers
├── analyzers/        # Analysis engines (unfinished projects, etc.)
├── exporters/        # Export modules (Obsidian, JSON, etc.)
└── cli.py           # Command-line interface
```

## Configuration

Create a `config.yaml` file to customize analysis parameters:

```yaml
analysis:
  unfinished_project:
    keywords:
      - "TODO"
      - "need to"
      - "should implement"
      - "next steps"
    min_confidence: 0.7

obsidian:
  vault_path: ~/Documents/ObsidianVault
  folder: "AI Projects"
```

## Extending

### Adding a New Platform

1. Create a parser in `parsers/your_platform.py`
2. Implement the `BaseParser` interface
3. Register in `parsers/__init__.py`

### Adding a New Analysis Type

1. Create an analyzer in `analyzers/your_analyzer.py`
2. Implement the `BaseAnalyzer` interface
3. Register in `analyzers/__init__.py`

