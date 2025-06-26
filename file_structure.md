# AskIT-CLI Code Structure

This document describes the source code structure for `askit-cli`. The architecture is designed to be modular, testable, and extensible, especially to allow for the easy addition of new AI providers.

```
askit-cli/
├── src/
│   └── askit/
│       ├── __init__.py
│       │
│       ├── cli.py             # Main entry point for the CLI (Typer)
│       │
│       ├── commands/          # Business logic for each CLI command
│       │   ├── __init__.py
│       │   ├── init_cmd.py    # 'init' command
│       │   ├── config_cmd.py  # 'config' command (interactive shell)
│       │   └── ...            # Other command files
│       │
│       ├── core/              # Core application logic
│       │   ├── __init__.py
│       │   ├── context_builder.py # Context building (file scanning, IaC parsing)
│       │   ├── history.py     # Shell history retrieval (multi-OS)
│       │   └── project.py     # Project root detection (.askit)
│       │
│       ├── security/          # Security-related modules
│       │   ├── __init__.py
│       │   ├── masking.py     # Masking of secrets and sensitive data (PII)
│       │   └── secrets_manager.py # Secure API key management (via OS keychain)
│       │
│       └── providers/         # Modular architecture for AI backends
│           ├── __init__.py
│           ├── base_provider.py # Abstract base class for all providers
│           ├── claude.py      # Implementation for Anthropic Claude
│           ├── openai.py      # Future implementation for OpenAI
│           └── ollama.py      # Future implementation for Ollama (local)
│
├── tests/                   # Unit and integration tests
│   ├── commands/
│   │   └── test_init_cmd.py
│   └── core/
│       └── test_context_builder.py
│
├── .gitignore
├── pyproject.toml           # Project metadata and dependencies (Poetry/Hatch)
├── README.md                # Main project documentation
└── file_structure.md        # This file
```

## Key Directory Descriptions

### `src/askit/`
This is the main Python package of the application, following modern conventions.

*   **`cli.py`**: Defines the CLI using `Typer`. It imports and orchestrates the different commands from the `commands` module.

*   **`commands/`**: Each file corresponds to a CLI command (e.g., `init`, `config`). This helps to properly isolate the logic for each user action. The filenames are suffixed with `_cmd` to avoid conflicts with Python module names.

*   **`core/`**: Contains the central and reusable business logic.
    *   `context_builder.py`: Manages project file scanning, parsing of IaC files (Ansible, Terraform), and assembling the context cache.
    *   `history.py`: Cross-platform code to read the user's shell history.
    *   `project.py`: Logic to find the project root by locating the `.askit` directory.

*   **`security/`**: Groups all security-related features.
    *   `masking.py`: Implements the detection and masking of sensitive data before it is sent to the AI API.
    *   `secrets_manager.py`: Provides an abstraction for securely storing and retrieving API keys via the native OS secret manager (Keychain, Credential Manager, etc.).

*   **`providers/`**: This directory is the key to modularity for AI backends.
    *   `base_provider.py`: Defines an abstract base class (e.g., `AIBaseProvider`) with common methods (`get_suggestion()`, `_prepare_prompt()`, etc.).
    *   Each other file (`claude.py`, `openai.py`) inherits from this base class and implements the logic specific to an AI service. To add a new provider, you just need to create a new file that respects this interface.

### `tests/`
Contains all unit and integration tests, mirroring the structure of the `src/` directory for easy navigation.

### Project Files
*   **`pyproject.toml`**: Standard file for managing dependencies and build configuration of the Python project.
*   **`README.md`**: The main documentation for the project.
*   **`file_structure.md`**: This file, serving as a map for navigating the source code. 