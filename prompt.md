# 🚀 Project: **AskIT-CLI**

---

## 🧭 **Functional Summary**

**AskIT-CLI** is an intelligent command-line assistance tool for **Admins, DevOps, SecOps, CloudOps, and InfraSec** teams.

The goal is to have a **cloud-native terminal copilot** that:

* Automatically retrieves the technical context of the current environment (IaC files, shell history).
* Interacts with an LLM (Claude, etc.) to generate commands, solutions, and suggestions.
* Offers a fast and secure execution workflow, controlled by the user.
* Protects secrets and sensitive data during exchanges with the AI.
* Is configured simply and intuitively, with guidance on the first run.

---

## 🎯 **Main Use Cases**

* **On-the-fly command generation**: "create a tar.gz archive of this folder"
* **Infrastructure queries**: "modify this terraform to add a public subnet"
* **Troubleshooting help**: "the kubernetes pod is in CrashLoopBackOff, what are the first verification steps?"
* **Security operations**: "create a firewall rule to allow port 443"

---

## ⚙️ **Technical Architecture**

| Feature           | Choice                                               |
| ----------------- | ---------------------------------------------------- |
| Main Language | **Python 3.12+**                                     |
| Standalone Build  | **PyInstaller (multi-platform via GitHub Actions)**  |
| LLM API           | Claude AI (by default), extensible                   |
| Supported Shells  | PowerShell, Bash, Zsh                                |
| Local Context    | Reading shell history and scanning IaC files |
| Security          | Masking secrets before sending to the API              |
| Configuration     | `config.yaml` file in an `.askit` directory    |

---

## 🔐 **Security & Anonymization**

* **Adaptive Secret Masking**: `api_key`, `token`, `secret`, `password`, `AWS_*`, etc. are detected and partially masked to never be sent in plaintext.
* **Execution Control**: No command is executed without user action (pressing `Enter` in `strike` mode, or manual confirmation).
* **`--safe` Flag**: An additional safeguard to block potentially destructive commands, even in `strike` mode.

---

## 🧠 **Key Features**

### 1️⃣ Direct and Fast Interaction

The core of AskIT-CLI is its single-line invocation. The `-p` argument captures all the text that follows it, eliminating the need for quotes. The `-c` argument provides immediate context from the shell history.

`askit-cli -c 10 -p my request in natural language`

### 2️⃣ Secure and Controlled Execution

The tool offers a simple execution `mode` to adapt to the user's confidence level:

*   **`strike` mode**: For speed. If the AI is 100% sure, the command is directly proposed for execution.
*   **`normal` mode**: For deliberation. Always offers suggestions without pre-filling the command line.

### 3️⃣ Guided and Intuitive Configuration

On the first run, if no `.askit` directory is detected, the tool suggests running `askit-cli init`. If the configuration file is incomplete, it launches the `config` menu to guide the user.

### 4️⃣ Context Management by `init`

The `init` command is the single entry point to **create or update** the project context. It creates the `.askit` directory which anchors the project root, then (re)scans the entire project to update the `context.json` cache.

---

## 🔩 **Proposed Starting Tech Stack**

| Tool            | Usage                               |
| ---------------- | ----------------------------------------- |
| `python 3.12+`   | Core app                                  |
| `typer`          | Modern CLI                               |
| `rich`           | Elegant terminal display                |
| `requests`       | API requests (Claude, OpenAI, etc.)       |
| `pyyaml`         | IaC & config parsing                      |
| `python-dotenv`  | Parsing of `.env` files               |
| `detect-secrets` | Detection of secrets in the code         |
| `prompt_toolkit` | Interactive configuration menu          |
| `pyinstaller`    | Standalone packaging                      |
| `github actions` | Multi-platform build & CI/CD              |

---

## 🚀 **MVP (Minimum Viable Product) Roadmap**

1️⃣ Basic CLI with argument parsing (`-p`, `-c`, `--safe`).
2️⃣ Implementation of the `init` command to create/update the project (`.askit`, config, cache).
3️⃣ Implementation of the `config` command and its interactive menu (management of `mode` and `api_key`).
4️⃣ Logic for execution modes (`strike`, `normal`) and the `--safe` flag.
5️⃣ Interaction with an LLM API (e.g., Claude).
6️⃣ Logic for displaying the command/suggestion and managing execution.
7️⃣ Context scan in the `init` command.
