# Usage Guide

## Getting Started

### 1. Export Your Chat Histories

First, you need to export your chat histories from each platform:

- **ChatGPT**: Go to Settings → Data Controls → Export Data
- **Claude**: Check Anthropic's export options in account settings
- **Gemini**: Use Google Takeout or check account settings

### 2. Install the Tool

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### 3. Run Your First Analysis

```bash
python -m ai_history_analyser analyze \
  --input chatgpt_export.json \
  --platform chatgpt \
  --output results.json
```

## Common Use Cases

### Finding Unfinished Projects

The default analyzer looks for unfinished projects by detecting keywords like:
- TODO, FIXME, XXX
- "need to", "should implement"
- "next steps", "not done"
- "unfinished", "incomplete"
- And many more...

### Exporting to Obsidian

If you use Obsidian for note-taking, you can export results directly:

```bash
python -m ai_history_analyser analyze \
  --input chatgpt.json --platform chatgpt \
  --obsidian \
  --obsidian-path ~/Documents/ObsidianVault
```

This will create:
- An index file: `Unfinished Projects Index.md`
- Individual project files for each unfinished project
- Properly formatted markdown with tags and metadata

### Analyzing Multiple Platforms

Combine histories from different platforms:

```bash
python -m ai_history_analyser analyze \
  --input chatgpt.json --platform chatgpt \
  --input claude.json --platform claude \
  --input gemini.json --platform gemini \
  --output combined_results.json
```

### Customizing Analysis

Create a `config.yaml` file to customize keywords and thresholds:

```bash
python -m ai_history_analyser init-config
```

Then edit `config.yaml` to adjust:
- Keywords to search for
- Minimum confidence threshold
- Obsidian export settings

## Understanding Results

### Priority Scores

Projects are scored from 0.0 to 1.0 based on:
- **Confidence**: How certain we are it's an unfinished project
- **Recency**: More recent projects score higher
- **Context**: More detailed projects score higher

### Confidence Scores

Confidence indicates how likely it is that this represents an unfinished project:
- **0.7-1.0**: Very likely unfinished
- **0.4-0.7**: Probably unfinished
- **0.0-0.4**: Possibly unfinished

## Future Analysis Types

The tool is designed to be extensible. Future analysis types could include:
- Sentiment analysis
- Topic clustering
- Time tracking
- Project completion tracking
- And more...

## Troubleshooting

### "Unsupported platform" error

Make sure you're using the correct platform name:
- `chatgpt` (not `chat-gpt` or `ChatGPT`)
- `claude` (not `Claude` or `anthropic`)
- `gemini` (not `Gemini` or `google-gemini`)

### No projects found

Try:
1. Lowering the confidence threshold in config
2. Adding more keywords to search for
3. Checking that your export file is in the correct format

### Parsing errors

Different platforms may export in slightly different formats. If parsing fails:
1. Check the export file is valid JSON
2. Try exporting again from the platform
3. Open an issue with a sample of your export format

