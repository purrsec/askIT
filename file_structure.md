# AskIT-CLI Code Structure

This document describes the source code structure for `askit-cli`. The architecture is designed to be modular, testable, and extensible, especially to allow for the easy addition of new AI providers.

```
askit-cli/
├── src/
│   └── askit/
│       ├── __init__.py
│       ├── _version.py         # Version information
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
│       │   ├── config_manager.py # Configuration management
│       │   ├── history.py     # Shell history retrieval (multi-OS)
│       │   └── project.py     # Project root detection (.askit)
│       │
│       ├── agent/             # AI agent runtime and execution
│       │   ├── __init__.py
│       │   └── runtime.py     # Agent execution logic
│       │
│       ├── security/          # Security-related modules
│       │   ├── __init__.py
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
│   └── test_cli.py          # Main CLI tests
│
├── run_cli.py               # Alternative entry point
├── .gitignore
├── pyproject.toml           # Project metadata and dependencies (Poetry)
├── poetry.lock              # Locked dependencies
├── README.md                # Main project documentation
├── CONTRIBUTING.md          # Contribution guidelines
├── INSTALL.md               # Installation instructions
├── LICENSE                  # License file
├── SECURITY.md              # Security policy
└── file_structure.md        # This file
```

## Key Directory Descriptions

### `src/askit/`
This is the main Python package of the application, following modern conventions.

*   **`cli.py`**: Defines the CLI using `Typer`. It imports and orchestrates the different commands from the `commands` module.

*   **`_version.py`**: Contains version information for the package.

*   **`commands/`**: Each file corresponds to a CLI command (e.g., `init`, `config`). This helps to properly isolate the logic for each user action. The filenames are suffixed with `_cmd` to avoid conflicts with Python module names.

*   **`core/`**: Contains the central and reusable business logic.
    *   `config_manager.py`: Manages application configuration and settings.
    *   `history.py`: Cross-platform code to read the user's shell history.
    *   `project.py`: Logic to find the project root by locating the `.askit` directory.

*   **`agent/`**: Contains the AI agent runtime and execution logic.
    *   `runtime.py`: Handles the execution and coordination of AI agent operations.

*   **`security/`**: Groups all security-related features.
    *   `secrets_manager.py`: Provides an abstraction for securely storing and retrieving API keys via the native OS secret manager (Keychain, Credential Manager, etc.).

*   **`providers/`**: This directory is the key to modularity for AI backends.
    *   `base_provider.py`: Defines an abstract base class (e.g., `AIBaseProvider`) with common methods (`get_suggestion()`, `_prepare_prompt()`, etc.).
    *   Each other file (`claude.py`, `openai.py`) inherits from this base class and implements the logic specific to an AI service. To add a new provider, you just need to create a new file that respects this interface.

### `tests/`
Contains all unit and integration tests for the application.

### Project Files
*   **`run_cli.py`**: Alternative entry point for running the CLI.
*   **`pyproject.toml`**: Standard file for managing dependencies and build configuration of the Python project.
*   **`poetry.lock`**: Locked dependencies file ensuring reproducible builds.
*   **`README.md`**: The main documentation for the project.
*   **`CONTRIBUTING.md`**: Guidelines for contributing to the project.
*   **`INSTALL.md`**: Installation instructions and setup guide.
*   **`LICENSE`**: Project license information.
*   **`SECURITY.md`**: Security policy and vulnerability reporting guidelines.
*   **`file_structure.md`**: This file, serving as a map for navigating the source code. 