# Changelog

## v0.1.9 - 2026-03-27

### Added
- Added `tests/test_evaluate.py` to cover edge cases for `evaluate_splits(...)` and `summarize_scores(...)`.
- Added `CONTRIBUTING.md` with the exact local workflow for install, lint, test, build, and release prep.

### Changed
- Polished the README with badges and a sharper explanation of the repo's purpose.
- Added a `Changelog` URL to package metadata.
- Bumped package version from `0.1.8` to `0.1.9`.

### Why this matters
- The repo now reads more like a finished public package and has slightly stronger verification/documentation around the public API.

## v0.1.8 - 2026-03-08

### Added
- Added `purge_by_horizon(...)` to the public package API for forward-horizon label leakage control.
- Added `drop_indices(...)` helper for applying embargo or custom blocked sets back onto training indices.
- Added tiny evaluation helpers: `accuracy_score`, `mean_score`, `evaluate_splits`, and `summarize_scores`.
- Added tests for leakage guards and evaluation helpers.

### Changed
- Updated `examples/leakage_demo.py` to use the real package API instead of carrying the most important leakage logic only inside the example.
- Updated README quickstart and install instructions.
- Bumped package version from `0.1.7` to `0.1.8`.
- Added `numpy` to development dependencies and an `examples` extra so the leakage demo works in a standard dev/example setup.

### Why this matters
- The repo's strongest idea — horizon-aware leakage control — is now part of the actual toolkit, not hidden only in an example script.
