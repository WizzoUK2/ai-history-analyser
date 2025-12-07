# Contributing to AI History Analyser

Thank you for your interest in contributing to AI History Analyser! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-history-analyser.git
   cd ai-history-analyser
   ```
3. **Set up the development environment**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Setup

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs additional tools like pytest, black, flake8, and mypy.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_history_analyser

# Run specific test file
pytest tests/test_parsers.py
```

### Code Style

We use `black` for code formatting and `flake8` for linting:

```bash
# Format code
black ai_history_analyser tests

# Check linting
flake8 ai_history_analyser tests
```

## Making Changes

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following the coding standards

3. **Test your changes**:
   ```bash
   python -m ai_history_analyser --help
   # Test with sample data
   python -m ai_history_analyser analyze --input test_data.json --platform chatgpt
   ```

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Pull Request Guidelines

- **Keep PRs focused**: One feature or fix per PR
- **Write clear descriptions**: Explain what and why, not just how
- **Update documentation**: If you add features, update README.md or USAGE.md
- **Add tests**: If possible, add tests for new functionality
- **Check CI**: Make sure all CI checks pass

## Areas for Contribution

We welcome contributions in these areas:

### New Platform Parsers

Add support for new AI platforms by:
1. Creating a new parser in `ai_history_analyser/parsers/`
2. Extending `BaseParser`
3. Registering it in `parsers/__init__.py`
4. Adding tests

### New Analyzers

Add new analysis types by:
1. Creating a new analyzer in `ai_history_analyser/analyzers/`
2. Extending `BaseAnalyzer`
3. Registering it in `analyzers/__init__.py`
4. Adding tests

### New Exporters

Add new export formats by:
1. Creating a new exporter in `ai_history_analyser/exporters/`
2. Extending `BaseExporter`
3. Registering it in `exporters/__init__.py`
4. Adding tests

### Bug Fixes

- Fix bugs in existing parsers/analyzers/exporters
- Improve error handling
- Fix compatibility issues

### Documentation

- Improve README.md
- Add more examples to USAGE.md
- Add docstrings to code
- Create tutorials or guides

### Testing

- Add unit tests
- Add integration tests
- Improve test coverage

## Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Reporting Bugs

If you find a bug, please open an issue with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Sample data (if applicable, anonymized)

## Feature Requests

For feature requests, please open an issue with:
- Description of the feature
- Use case or motivation
- Proposed implementation (if you have ideas)

## Questions?

Feel free to open an issue for questions or discussions. We're happy to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

