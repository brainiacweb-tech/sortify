# Contributing to Smart File Organizer (Sortify)

Thank you for your interest in contributing to Smart File Organizer!

## Guidelines
1. **Safety First**: Never perform direct destructive file mutations without dry-run validation and collision resolution.
2. **Architecture**: Keep UI components isolated from core business logic. All file operations must pass through `app/core/organizer.py` and `app/core/file_operations.py`.
3. **Tests**: All new features or bug fixes must include unit tests in `tests/` and pass `python -m pytest`.
4. **Code Style**: Follow PEP 8 guidelines and use Python type annotations (`typing` module / standard types).
