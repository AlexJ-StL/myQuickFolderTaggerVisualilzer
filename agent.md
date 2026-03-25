# Agent Directives

## Environment
- **OS**: Windows 11
- **Python Version**: 3.14
- **Package Manager**: `uv`
- **Linting & Formatting**: `ruff`

## Project Principles
- **Modularity**: Visualizer scripts must be modular, accepting DataFrames instead of loading data directly.
- **Privacy**: No hardcoded absolute paths. Use relative paths or truncate them securely using `PATH_MARKERS` in `config.py`.
- **Cross-Platform**: Do not hardcode `\` or `/`. Use `os.path.normpath`, `pathlib`, or `os.sep`.
- **Execution**: The single point of entry is `main.py`.
