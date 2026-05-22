# AI Research Assistant CLI

A learning-oriented command-line AI research assistant.

This project is part of a Python engineering and Claude Code learning path. The goal is to build a small but well-structured AI CLI project step by step, while practicing Python engineering, configuration management, prompt design, testing, documentation, and safe API key handling.

## Goal

Build a command-line tool that can help with research and study workflows.

The final project should be able to:

- Read text-based notes (.txt and .md)
- Summarize notes
- Answer questions about notes
- Generate follow-up research tasks
- Save interaction history

## Current Status

Project initialized with CLI skeleton, mock AI client, configuration layer, real Claude API integration, structured prompt engineering, and output saving.

Currently supported commands:

```bash
research --help
research [--verbose|-v] summarize <file> [--save]
research [--verbose|-v] ask <file> "<question>" [--save]
research [--verbose|-v] tasks <file> [--save]
research [--verbose|-v] history
```

Current behavior:

- Mock mode (default): returns placeholder responses
- Real mode: calls Claude API via Anthropic Python SDK with structured prompts
- `--save` flag saves output to `outputs/` directory
- `--verbose` flag enables debug logging and detailed error output
- Friendly error messages for all failure cases (no raw tracebacks)

## Project Structure

```text
ai-research-assistant-cli/
├── README.md
├── CLAUDE.md
├── Makefile
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── docs/
│   └── design.md
├── examples/
│   └── sample_note.md
├── src/
│   └── research_assistant/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── file_loader.py
│       ├── logger.py
│       ├── output_writer.py
│       ├── prompts.py
│       └── ai_client.py
└── tests/
    ├── __init__.py
    ├── test_ai_client.py
    ├── test_cli_errors.py
    ├── test_config.py
    ├── test_exceptions.py
    ├── test_file_loader.py
    ├── test_logger.py
    ├── test_output_writer.py
    └── test_prompts.py
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

## Usage

Show help:

```bash
research --help
```

Summarize a file:

```bash
research summarize examples/sample_note.md
```

Ask a question about a file:

```bash
research ask examples/sample_note.md "What is the main topic?"
```

Generate study tasks:

```bash
research tasks examples/sample_note.md
```

Show history:

```bash
research history
```

### Saving Output

Save summarize result to file:

```bash
research summarize examples/sample_note.md --save
# Output saved to: outputs/sample_note_summarize.md
```

Save ask result to file:

```bash
research ask examples/sample_note.md "What is self-attention?" --save
# Output saved to: outputs/sample_note_ask.md
```

Save tasks result to file:

```bash
research tasks examples/sample_note.md --save
# Output saved to: outputs/sample_note_tasks.md
```

### Output Examples

**Summarize:**
```bash
research summarize examples/sample_note.md
```
Expected output (real mode):
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
```bash
research ask examples/sample_note.md "What is self-attention?"
```
Expected output (real mode):
```
## Answer

Self-attention allows the model to weigh the importance of different words in a sentence when processing each word.

## Evidence from the Note

> "Self-attention allows the model to weigh the importance of different words in a sentence when processing each word."

## Caveats

- The note provides a high-level overview without mathematical details
```

**Tasks:**
```bash
research tasks examples/sample_note.md
```
Expected output (real mode):
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

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RESEARCH_ASSISTANT_MODE` | AI mode: `mock` or `real` | `mock` |
| `ANTHROPIC_API_KEY` | Anthropic API key (required for real mode) | - |
| `RESEARCH_ASSISTANT_MODEL` | Claude model name | `claude-sonnet-4-20250514` |

### Using Mock Mode (Default)

No configuration needed. The CLI works out of the box with mock responses:

```bash
research summarize examples/sample_note.md
# Output: [Mock Summary] This is a placeholder summary...
```

### Using Real Mode (Claude API)

```bash
export RESEARCH_ASSISTANT_MODE="real"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export RESEARCH_ASSISTANT_MODEL="claude-sonnet-4-20250514"  # optional
```

Get your API key from: https://console.anthropic.com/

If you set `RESEARCH_ASSISTANT_MODE=real` without providing an API key, you'll get a clear error message.

### API Key Safety

- Never commit API keys to Git
- Never hardcode API keys in source code
- Use environment variables only
- Add `.env` to `.gitignore`
- Never print API keys in logs or error messages

## Error Handling

The CLI provides friendly error messages instead of Python tracebacks:

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

### Verbose Mode

Use `--verbose` (or `-v`) to see detailed debug output:

```bash
# Verbose with long flag
research --verbose summarize examples/sample_note.md

# Verbose with short flag
research -v summarize examples/sample_note.md

# Verbose with any subcommand
research -v ask examples/sample_note.md "What is self-attention?"
```

Verbose mode shows internal steps like API call details and output file paths. For unexpected errors, `--verbose` shows the full traceback for debugging.

Verbose mode never prints API keys or file contents.

## Testing

Run tests:

```bash
pytest -q
```

Or use Makefile:

```bash
make test
```

## Makefile Commands

```bash
make install
make test
make help
make clean
```

Command meanings:

- `make install`: install the project and development requirements
- `make test`: run the test suite
- `make help`: show CLI help
- `make clean`: remove Python cache and build artifacts

## Engineering Goals

This project is designed to practice:

- Python project structure
- CLI development
- Environment variable handling
- Safe API key management
- Prompt template organization
- AI client abstraction
- Testable module design
- Error handling
- Documentation-first development
- Git and GitHub workflow
- Docker and CI in later lessons

## Development Rules

Before changing behavior:

1. Inspect the current project state
2. Make a small plan
3. Modify only the necessary files
4. Run tests
5. Review `git diff`
6. Update documentation if behavior changes
7. Commit with a clear message

Claude Code should not automatically commit changes.

## Learning Notes

This project starts simple on purpose.

The first milestone is not to build a powerful AI agent immediately. The first milestone is to create a clean, testable, maintainable Python CLI foundation. AI API integration will be added only after configuration, prompt structure, and testing strategy are ready.
