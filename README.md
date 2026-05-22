# AI Research Assistant CLI

[![CI](https://github.com/RayHe42/ai-research-assistant-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/RayHe42/ai-research-assistant-cli/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)

A command-line AI research assistant for reading notes, generating summaries, answering questions, and creating study tasks. Built as a learning project to practice Python engineering, CLI development, prompt design, and safe API integration.

## Features

- **Summarize** notes with key points, terms, and follow-up questions
- **Ask** questions about notes with evidence-based answers
- **Generate tasks** for further study with difficulty estimates
- **Mock mode** works out of the box -- no API key needed
- **Real mode** connects to Claude API via Anthropic SDK
- **--save** flag persists output to files
- **--verbose** flag enables debug logging
- **Friendly error messages** for all failure cases (no raw tracebacks)
- **98 automated tests** with GitHub Actions CI

## Engineering Highlights

- Clean module separation (8 modules, single responsibility)
- Abstract AI client with mock/real switching via factory pattern
- Structured prompt engineering with per-command output formats
- Custom exception hierarchy with unified error handling
- Security-first: API keys never logged, hardcoded, or leaked
- Environment-only configuration (no .env files)
- Full test coverage with pytest, monkeypatch, and tmp_path
- GitHub Actions CI on every push and pull request

## Installation

```bash
git clone https://github.com/RayHe42/ai-research-assistant-cli.git
cd ai-research-assistant-cli
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

### Mock Mode (Default)

No configuration needed. Works immediately with placeholder responses:

```bash
research summarize examples/sample_note.md
# Output: [Mock Summary] This is a placeholder summary...

research ask examples/sample_note.md "What is the main topic?"
# Output: [Mock Answer] This is a placeholder answer...

research tasks examples/sample_note.md
# Output: [Mock Tasks] These are placeholder tasks...
```

### Real Mode (Claude API)

```bash
export RESEARCH_ASSISTANT_MODE="real"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export RESEARCH_ASSISTANT_MODEL="claude-sonnet-4-20250514"  # optional
```

Get your API key from: https://console.anthropic.com/

If you set `RESEARCH_ASSISTANT_MODE=real` without providing an API key, you'll get a clear error message.

### Saving Output

Use `--save` to persist results to the `outputs/` directory:

```bash
research summarize examples/sample_note.md --save
# Output saved to: outputs/sample_note_summarize.md

research ask examples/sample_note.md "What is self-attention?" --save
# Output saved to: outputs/sample_note_ask.md

research tasks examples/sample_note.md --save
# Output saved to: outputs/sample_note_tasks.md
```

### Verbose Mode

Use `--verbose` or `-v` to see detailed debug output:

```bash
research --verbose summarize examples/sample_note.md
research -v ask examples/sample_note.md "What is self-attention?"
```

Verbose mode shows internal steps like API call details and output file paths. For unexpected errors, `--verbose` shows the full traceback for debugging. Verbose mode never prints API keys or file contents.

### Command Reference

```bash
research --help
research [--verbose|-v] summarize <file> [--save]
research [--verbose|-v] ask <file> "<question>" [--save]
research [--verbose|-v] tasks <file> [--save]
research history
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `RESEARCH_ASSISTANT_MODE` | AI mode: `mock` or `real` | `mock` |
| `ANTHROPIC_API_KEY` | Anthropic API key (required for real mode) | - |
| `RESEARCH_ASSISTANT_MODEL` | Claude model name | `claude-sonnet-4-20250514` |

## Error Handling

| Error | User sees |
|-------|-----------|
| File not found | `Error: File not found: path/to/file` |
| Unsupported file type | `Error: Unsupported file type: .csv. Supported types: .md, .txt` |
| Empty file | `Error: File is empty: path/to/file` |
| Invalid mode | `Error: Invalid RESEARCH_ASSISTANT_MODE=foo. Must be one of: mock, real` |
| Missing API key | `Error: RESEARCH_ASSISTANT_MODE is 'real', but ANTHROPIC_API_KEY is not set.` |
| API authentication failed | `Error: API authentication failed. Check your ANTHROPIC_API_KEY.` |
| API rate limit | `Error: API rate limit exceeded. Please try again later.` |
| Output save failed | `Error: Failed to save output to outputs: ...` |

All errors exit with code 1.

## API Key Safety

- Never commit API keys to Git
- Never hardcode API keys in source code
- Use environment variables only
- Never print API keys in logs or error messages
- Verbose mode never exposes keys, file contents, or prompt text

## Project Structure

```text
ai-research-assistant-cli/
├── README.md
├── CLAUDE.md
├── CHANGELOG.md
├── Makefile
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── design.md
├── examples/
│   └── sample_note.md
├── src/
│   └── research_assistant/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point, argument parsing, error handling
│       ├── config.py           # Environment variable configuration
│       ├── exceptions.py       # Custom exception hierarchy
│       ├── file_loader.py      # Read .txt / .md files
│       ├── logger.py           # Logging setup (setup_logger, get_logger)
│       ├── output_writer.py    # Save output to files
│       ├── prompts.py          # Structured prompt templates
│       └── ai_client.py        # AI client abstraction + mock + Claude API
└── tests/
    ├── __init__.py
    ├── test_ai_client.py
    ├── test_cli.py
    ├── test_cli_commands.py
    ├── test_cli_errors.py
    ├── test_config.py
    ├── test_exceptions.py
    ├── test_file_loader.py
    ├── test_logger.py
    ├── test_output_writer.py
    └── test_prompts.py
```

## Testing

```bash
pytest -q
```

Or use Makefile:

```bash
make test
```

All tests run in mock mode -- no real API calls are made, and no API key is required.

### CI

Every push and pull request to `main` automatically runs the test suite via GitHub Actions. The CI workflow:

1. Sets up Python 3.11 on Ubuntu
2. Installs project dependencies
3. Runs `pytest -q`
4. Uses mock mode (no API key needed)

## Makefile Commands

```bash
make install   # Install project and dev requirements
make test      # Run test suite
make help      # Show CLI help
make clean     # Remove Python cache and build artifacts
```

## Output Examples

**Summarize:**
```
## Summary

The Transformer is a deep learning architecture that uses self-attention mechanisms instead of recurrent neural networks...

## Key Points

- Self-attention allows weighing importance of different words
- Multi-head attention attends to different representation subspaces
- Positional encoding provides sequence position information

## Terms

- Self-Attention: Mechanism to weigh word importance in context
- Multi-Head Attention: Multiple attention functions in parallel

## Follow-up Questions

1. How does self-attention scale with sequence length?
2. What are the computational advantages over RNNs?
```

**Ask:**
```
## Answer

Self-attention allows the model to weigh the importance of different words in a sentence when processing each word.

## Evidence from the Note

> "Self-attention allows the model to weigh the importance of different words in a sentence when processing each word."

## Caveats

- The note provides a high-level overview without mathematical details
```

**Tasks:**
```
## Learning Tasks

1. [Reading] Read the original "Attention Is All You Need" paper
2. [Writing] Write a comparison between Transformer and RNN architectures
3. [Practice] Implement a simple self-attention mechanism in Python

## Suggested Order

- Start with: Task 1 because it provides foundational understanding
- Then: Task 2 because it deepens conceptual understanding
- Finally: Task 3 because it requires practical implementation skills

## Estimated Difficulty

- Task 1: Medium
- Task 2: Medium
- Task 3: Hard
```

## License

This project is for learning purposes.
