# Contributing

## Local development

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Quality checks

```bash
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe examples\demo_naive_vs_purged.py
.\.venv\Scripts\python.exe examples\leakage_demo.py
python -m build
```

## Release checklist

1. Update `CHANGELOG.md`.
2. Bump version in `pyproject.toml`.
3. Ensure CI is green on the release PR.
4. Merge to `main`.
5. Tag the release and publish GitHub release notes.
