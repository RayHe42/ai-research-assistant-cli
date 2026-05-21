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

Project initialized with CLI skeleton and mock AI client.

Currently supported commands:

```bash
research --help
research summarize <file>
research ask <file> "<question>"
research tasks <file>
research history
```

Current behavior:

- `research summarize notes.md` — prints a mock summary
- `research ask notes.md "What is X?"` — prints a mock answer
- `research tasks notes.md` — prints mock study tasks
- `research history` — prints "No history yet."
- AI API integration is not implemented yet (uses MockClient)

## Planned Features

- Connect to real AI API (Claude, OpenAI, etc.)
- Save interaction history to JSON
- Add prompt templates
- Add error handling
- Add Docker support
- Add GitHub Actions CI

## Non-Goals for the First MVP

The first version will not include:

- PDF parsing
- Web UI
- Database
- RAG
- Multi-agent workflow
- User accounts
- Deployment

These can be added later after the core CLI and AI workflow are stable.

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
│       ├── file_loader.py
│       ├── prompts.py
│       └── ai_client.py
└── tests/
    ├── __init__.py
    ├── test_file_loader.py
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

## Configuration

Future AI API integration should use environment variables.

Example:

```bash
export AI_API_KEY="..."
```

API keys must never be committed to Git.

Do not commit:

- `.env`
- `.env.*`
- API keys
- local data
- generated cache files

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
