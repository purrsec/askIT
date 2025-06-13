# 🚀 Project: AskIT-CLI

**AskIT-CLI** is an intelligent command-line assistant, designed to be fast, efficient, and context-aware. It simplifies administrative tasks by allowing you to use natural language to generate and execute shell commands, all while staying in your terminal.

---

## 🔥 Simplified Workflow

### First Use

The `askit-cli init` command is the starting point. It initializes your project by creating an `.askit` directory. Then, it launches an intelligent process to build the context:
*   **Automatic Scan:** It searches for key files like Ansible inventories, Terraform files, etc.
*   **Interactive Questionnaire:** To complete the information, `init` asks you a few questions about the project's objectives, technical stack, and conventions.

Everything is stored in configuration and cache files within the `.askit` directory.

If you run `askit-cli` without an `.askit` directory being found in the current folder or its parents, the tool will suggest running `init` to get started.

### Daily Use

1.  **Make your request**: From any folder in your project, formulate a request in a single line.

    ```bash
    askit-cli -c 10 -p modify the terraform file to add a private VPC with a public subnet
    ```
    *   `-c 10`: Provides the last 10 commands from your shell history as context.
    *   `-p`: Everything that follows is your instruction (prompt), without needing quotes.

2.  **Receive the answer**: AskIT-CLI analyzes your request with the context and offers a solution.

    *   **Case 1: 100% confidence (and `strike` mode)**
        The tool is certain of the command to execute. It displays it directly in your terminal, ready to be validated.
        ```bash
        > sudo ufw allow 443/tcp
        [Press Enter to execute, or Ctrl+C to cancel]
        ```
        You just have to press **Enter** to run it.

    *   **Case 2: Doubt or `normal` mode**
        The tool is not certain, or you are in `normal` mode. It displays a suggestion that you can freely copy, modify, or ignore.
        ```bash
        > Suggestion: check existing rules before adding a new one.
        ```
---

## ⚙️ Key Commands & Arguments

| Action                | Description                                                          | Type      | Example                                        |
| --------------------- | -------------------------------------------------------------------- | --------- | ---------------------------------------------- |
| `init`                | Initializes or updates the project: creates the `.askit` directory and (re)generates the context cache. | Command   | `askit-cli init`                               |
| `config`              | Opens the interactive configuration menu (Cisco style).              | Command   | `askit-cli config`                             |
| `-p <prompt>`         | **(Required)** The user prompt. Must be the last argument. | Argument  | `askit-cli -p "add a public subnet"`                  |
| `-c <number>`         | Number of shell history lines to send as context.        | Argument  | `-c 10`                                        |
| `--safe`              | Activates "Safe Mode" (rejects commands deemed risky).        | Argument  | `askit-cli --safe -p "delete the cache"`     |

---

## 🧠 Context & Cache

`askit-cli` finds the project root by looking for an `.askit` directory. This folder contains all the context.

The `init` command is the heart of the context system. Instead of asking you to maintain a manual file, `init` automates information gathering:

1.  **Ansible Compatibility:** It parses Ansible inventory files (`inventory`, `hosts.yml`, etc.) to understand your infrastructure, host groups, and variables.
2.  **Terraform Analysis:** It reads your `.tf` and `.tfvars` files to learn about your providers, resources, and modules.
3.  **Configuration Questionnaire:** If information is missing, `init` launches an interactive setup to define non-detectable elements:
    - The main objective of the project.
    - Specific security rules (e.g., `"Never run terraform destroy"`).
    - Frequently used custom aliases or scripts.

The collected information is stored in `.askit/config.yaml` (questionnaire answers, configuration) and `.askit/context.json` (content of scanned files). You can re-run `init` at any time to update the context.

This approach allows for **cross-directory** reading: you can be in a `terraform/` subdirectory and `askit-cli` will be aware of the `ansible/inventory` file located elsewhere in the project.

---

## 🎛️ Configuration (Cisco CLI Style)

For fine-tuned configuration familiar to network/system administrators, use the `config` command.

```bash
askit-cli config
```

This opens an interactive menu where you can use simple and clear commands:

| Command                  | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| `set mode <strike\|normal>` | Sets the global operating mode.                                |
| `set api_key`            | Opens a secure prompt for your API key. It will **never** be stored in plaintext in `config.yaml`. |
| `show config`            | Displays the current configuration (the API key is masked).              |
| `exit`                   | Exits the configuration menu.                                         |

The tool will always look for an API key via an environment variable first (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`). The `set api_key` command is an alternative that securely stores the key in the OS keychain (credential manager).

---

## 🛡️ Security Modes

Execution logic is controlled by a single parameter: the `mode`.

*   **`normal` mode (default)**: The tool offers suggestions but never pre-fills your command line. This is the safest mode.
*   **`strike` mode**: If the AI's confidence is 100%, the command is directly inserted into your terminal, ready for execution with the **Enter** key. This is the fastest mode.
*   **`--safe` flag**: Can be added to any command to override the behavior and prevent the execution of any command deemed risky (e.g., `rm -rf`, `terraform destroy`), even in `strike` mode.

---

## 📝 Golden Rules

1.  The `-p` argument must **always** be the last one.
2.  Everything following `-p` is considered the raw prompt. No quotes are needed.
3.  If you use `-c`, it must be placed before `-p`.
4.  Direct execution of a command is only possible in **`strike` mode** with a **100% confidence level**. In all other cases, confirmation or manual action is required.

---

## 🎯 Main Use Cases

* Interactive assistance for cloud administration
* Secure generation of shell commands
* System error correction
* Automation suggestions
* Infrastructure verification (ansible, terraform, k8s, cloud)
* Support for SecOps / forensic operations
* Preparation of dynamic playbooks and runbooks

---

## CLI Usage

### General Structure
```bash
askit-cli [command] [options] -p "user prompt"
```

### Supported Commands

| Command    | Description                                                |
| ----------- | ---------------------------------------------------------- |
| `init`      | Initializes the AskIT-CLI project in the current directory |
| `history`   | Reads the shell history of the current terminal                 |
| `scan`      | Scans Ansible, Terraform, README.md, .env files    |
| `prompt`    | Allows direct interaction with Claude                 |
| `dry-run`   | Simulates generated commands without executing them            |
| `execute`   | Automatic execution mode with human confirmation       |
| `autopilot` | Automatic iterative mode: proposes, validates, and executes     |
| `config`    | Allows configuration of the API key and global options         |
| `status`    | Summarizes the current state of the loaded context                    |
| `reset`     | Clears the local project cache/context                    |
| `update`    | Updates AskIT-CLI itself                              |

### Global Arguments

| Argument          | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `-h`              | Displays the full help for AskIT-CLI                                     |
| `-v`              | Displays the version                                                       |
| `-d` or `--debug` | Debug mode with detailed logs                                           |
| `-p`              | User prompt to pass to the AI (must be at the end of parsing) |
| `-c`              | History context size (default: last 10 commands)           |
| `--strict-mode`   | The AI only suggests a command if it is certain                    |
| `--safe-mode`     | Aggressively masks secrets before sending                             |
| `--no-exec`       | Never execute commands automatically                          |
| `--logfile`       | Path to a local log file                                         |
| `--backend`       | Allows choosing the AI backend (`claude`, `openai`, etc.)               |
| `--prompt-file`   | Load a text file as a prompt instead of `-p`              |

**Important:** The `-p` argument must always be the last one to avoid parsing ambiguities.

### Example Call

```bash
askit-cli scan -c 15 --strict-mode --safe-mode -p Prepare the infrastructure migration to a multi-AZ VPC with managed high-availability PostgreSQL
```

---

## 🧠 Features

### General Operation

1️⃣ Automatic scan of the current project
2️⃣ Dynamic construction of the full context
3️⃣ Generation of the enriched prompt
4️⃣ Call to the Claude API (or selected AI backend)
5️⃣ Presentation of the result in 2 forms:
    * **100% safe single command** ➔ execution possible
    * **Partial suggestion** ➔ requests user confirmation
6️⃣ Local logging for audit

### Project Context Detection

On startup, AskIT-CLI scans the current directory for files like:
* `ansible.cfg`, `inventory`, `*.yml`
* `terraform.tf`, `*.tf`, `*.tfvars`
* `README.md`
* `*.env`, `config.yaml`, `*.ini`

### Interactive `init`

On the first run or on demand, the `init` command asks the administrator a series of questions to configure the project context. The answers are stored in `.askit/config.yaml` and serve as a permanent guide for the AI.

### Shell History Management

Native history retrieval on Bash, Zsh, PowerShell.

### Secure Execution

The user validates or edits the command proposed by the AI before execution (unless the `--confirm` option is used).

### *AutoPilot* Mode

Iterative mode for automatic problem correction, where each command is tested and validated.

---

## 🔐 Security & Anonymization

* **Adaptive Secret Masking**: Secrets (`api_key`, `token`, `password`, `AWS_*`, etc.) are partially masked before being sent to the AI to avoid leaking sensitive information.
* **No leakage of full values** in prompts.
* **Local audit** of proposed commands.
* **Logging** possible for SecOps audit.
* **PII Detection**: Neutralization of any sensitive personal data.

---

## 🗂 Project File Structure (after `init`)

```
.
└── .askit/
    ├── config.yaml      # Project configuration (mode, objectives). Contains **no** secrets.
    ├── context.json     # Context cache (content of scanned IaC files)
    ├── scan-report.md   # Report of the last file scan
    └── logs/
        └── session-YYYYMMDD-HHMM.log # Log of commands and responses
```

---

## ⚙️ Architecture & Tech Stack

### Architecture

| Feature           | Choice                                               |
| ----------------- | --------------------------------------------------- |
| Main Language | **Python 3.12+**                                    |
| Standalone Build  | **PyInstaller (multi-platform via GitHub Actions)** |
| Packaging         | `.exe` / `.bin` / `.app` binary                    |
| LLM API           | Claude AI (Anthropic Cloud) - (extensible)          |
| CLI Framework     | **Typer**                                           |
| Config Management | **YAML** + Interactive Menu                         |
| Secret Storage    | **OS Keychain** (via `keyring` library)             |

### Dependencies

| Library           | Purpose                                     |
| ----------------- | ------------------------------------------- |
| `typer`           | CLI creation                              |
| `rich`            | Rich text formatting in the terminal      |
| `pyyaml`          | YAML parsing for configuration            |
| `anthropic`       | Official client for the Claude API        |
| `keyring`         | Secure secret storage                     |
| `inquirer`        | Interactive menus and questions           |
| `watchdog`        | (Optional) File system monitoring         |

> This project is a proof-of-concept and a work in progress.

---

Feel free to contribute or report issues! 