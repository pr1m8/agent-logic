# Contributing to agent-logic

Thanks for helping improve **agent-logic**! We welcome features, fixes, docs, and examples.

## Local Development
```bash
git clone https://github.com/pr1m8/agent-logic.git
cd agent-logic
poetry install
poetry run pytest -q
```

## Style & Quality
- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- **Tests**: `pytest -q` (seed where randomness exists)
- **Lint**: `ruff format .` + `ruff check .`
- **Types**: `pyright` or `mypy` for public APIs
- **Docs**: Google-style docstrings, examples for new functions

## PR Checklist
- [ ] Tests pass locally
- [ ] Lint + type checks are clean
- [ ] Examples / docs updated (if user-facing)
- [ ] No breaking changes (or documented)

## Issues
Please include:
- Minimal repro (code + expected vs actual)
- Environment (OS, Python, package versions)
- Logs or stack traces
