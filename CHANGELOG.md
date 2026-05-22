# Changelog

## [0.1.0] - 2026-05-22

### Added

#### CLI Commands
- `research summarize <file>` -- generate summaries with key points, terms, and follow-up questions
- `research ask <file> "<question>"` -- answer questions with evidence-based responses
- `research tasks <file>` -- generate study tasks with difficulty estimates
- `research history` -- show interaction history (placeholder for future persistence)

#### AI Integration
- Mock mode (default) for development without API key
- Real mode with Claude API integration via Anthropic SDK
- Factory pattern for switching between mock and real clients
- Structured prompt templates per command (summarize, ask, tasks)

#### Output & Debugging
- `--save` flag to persist output to `outputs/` directory
- `--verbose` / `-v` flag for debug logging
- Friendly error messages for all failure cases (no raw tracebacks)

#### Configuration
- Environment variable configuration (`RESEARCH_ASSISTANT_MODE`, `ANTHROPIC_API_KEY`, `RESEARCH_ASSISTANT_MODEL`)
- Custom exception hierarchy (`ResearchAssistantError` -> `FileLoadError`, `ConfigError`, `AIClientError`, `OutputWriteError`)

#### Engineering
- 98 automated tests with pytest (mock mode, no API key required)
- GitHub Actions CI on push and pull request to main
- src layout with pyproject.toml
- Makefile for common commands (install, test, clean, help)
- Security-first logging (API keys, file contents, and prompts never logged)
- Design document (`docs/design.md`)
