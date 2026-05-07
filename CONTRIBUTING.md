# Contributing to AI SaaS Kit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, open a new issue with:
   - A clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the use case and expected behavior
3. Be open to discussion and feedback

### Pull Requests

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/ai-saas-kit.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes** — keep them focused and atomic
5. **Write tests** for any new functionality
6. **Run the test suite**: `pytest`
7. **Lint your code**: `ruff check .`
8. **Commit** with clear messages: `git commit -m "Add feature: description"`
9. **Push** to your fork: `git push origin feature/your-feature-name`
10. **Open a Pull Request** against the `main` branch

## Code Style

- Follow PEP 8 conventions
- Use type hints where appropriate
- Keep functions small and focused
- Write docstrings for public functions and classes
- Line length: 120 characters
- Use `ruff` for linting: `ruff check .`

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-saas-kit.git
cd ai-saas-kit
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your settings
pytest  # Run tests
python run.py  # Start dev server
```

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
