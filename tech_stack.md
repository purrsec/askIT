Perfect. Now we're getting into **"industrial AI CLI design,"** exactly what we'd do if we were working on this with several devs in a real feature team.

I will now write an **"AI-friendly" technical specification** that will serve as documentation for the AI that will code this tool.
It will contain:

* The CLI structure
* Argument parsing rules
* Expected behaviors
* Important constraints for robust parsing
* Future features already considered

---

# 📄 **AskIT-CLI Technical Specification (for AI Developer)**

---

## 🧭 Application Name

**askit-cli**

---

## 🎯 Application Objective

An AI-driven cloud-native assistant for:

* System Administrators
* DevOps
* SecOps
* CloudOps

The goal is to **read the local context** (IaC, README, shell history), prepare an enriched prompt for an AI (e.g., Claude API), and securely generate the necessary commands with conditional execution logic. The workflow is optimized for speed and ease of use directly from the terminal.

---

## 🧩 General CLI Structure

```
askit-cli [command] [options] -p <user_prompt>
```

---

## 📚 **Supported Commands**

| Command | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| `init`   | Initializes or updates the project: creates the `.askit` directory and (re)generates the context cache. |
| `config` | Opens the AskIT-CLI configuration menu                        |

---

## 🔧 **Global Arguments**

| Argument      | Description                                                    | Position            |
| ------------- | -------------------------------------------------------------- | ------------------- |
| `-c <number>` | Number of shell history lines to send                  | Before `-p`          |
| `-p <prompt>` | User prompt (everything that follows is taken as the prompt)    | Must be the last|
| `--safe`      | "Safe Mode" (rejects risky commands), overrides `strike` mode. | Anywhere             |

---

## ⚠ **Important for AI during Parsing**

* **Always require `-p` to be the last argument** to avoid parsing ambiguities.
* All other arguments/options must be placed before `-p`.
* Warn the user if arguments are placed after `-p`.

---

## 🗂 **Project File Structure (post-init)**

The `init` command creates the following structure at the project root:

```
.
└── .askit/
    ├── config.yaml   # Configuration (modes, API key, etc.)
    └── context.json  # Context cache for IaC/DevOps files.
```

---

## 🎛️ **Cisco-Style CLI Configuration**

The `askit-cli config` command opens an interactive configuration menu to modify `.askit/config.yaml`.

### Configuration Commands

*   `set mode <strike|normal>`: Change the execution mode.
*   `set api_key <key>`: Set the API key.
*   `show config`: Display the current configuration.

---

## 📄 **Scanning Rules**

1.  **Project Root Detection**: The tool must find the project root by searching upwards for an `.askit` directory. If not found, suggest the user run `askit-cli init`.
2.  **Cross-Directory Scan**: The `init` command is the single command to (re)scan the entire directory tree from the project root. The user must run it manually to refresh the context.
3.  **Caching**: The contents are stored in `.askit/context.json`.

| File Type                  | Action                                    |
| -------------------------------- | ----------------------------------------- |
| `*.tf, *.tfvars`                 | Extract declared cloud resources |
| `*.yml, *.yaml`                  | Extract Ansible tasks              |
| `README.md`                      | Direct inclusion in the context        |
| `.env, config.yaml`              | Extract environment variables  |
| `package.json, requirements.txt` | Identify dependencies for info      |
| `inventory` (Ansible)            | Identify hosts, groups             |
| `*.kube/config`                  | Load Kubernetes context if it exists   |

---

## 🛡 **AI Security**

* Before sending to the AI:

  * Partially mask secrets (example: `AZURE_KEY=sk-abc...xyz`)
  * Never send full credentials.
  * Automatically detect and neutralize any sensitive PII data.
  * Show the user a summary of what is being sent (with `--debug` option).

---

## 🔬 **Potential Future Features**

* Plugin architecture (add specific cloud modules: AWS, Azure, GCP)
* Cloud provider SSO integration to retrieve project metadata
* CI/CD integration hooks to enrich the context
* Multi-user profile support
* Auto-documentation of AskIT sessions
* Secrets manager integration
* Infrastructure "pair-programming" mode

---

## 🖼 Full Example Call

```bash
askit-cli -c 15 --strike -p create a firewall rule to allow port 443
```

---

## 🧪 General Operation

1.  **Project Detection**: Look for the `.askit` directory in parent directories. If not found, prompt the user to run `init` and stop the flow.
2.  **Configuration Check**: Read `.askit/config.yaml`. If the API key is missing, launch the `config` command and stop the flow.
3.  **Context Retrieval**: Load shell history (via `-c`) and the content of the `.askit/context.json` cache.
4.  **Send Context + Prompt** to the LLM's API.
5.  **Receive and Analyze** the response.
6.  **Present the Result** to the user, based on the `mode` (`strike` or `normal`) and the `--safe` flag.

*   **Case 1 (`strike` mode AND 100% confidence AND not blocked by `--safe`)**: The command is displayed, ready to be executed.
*   **Case 2 (Others)**: A readable suggestion is displayed.
7.  **Local Logging** of the session for auditing.

---

## 🛠 Recommended Tech Stack

* `python 3.12+`
* `typer`
* `rich`
* `prompt_toolkit`
* `requests`
* `pyyaml`
* `pyperclip`
* `detect-secrets` (to detect secrets in the code)
* `gitpython` (to get info about the local repo)
* `python-dotenv` (parsing .env)
* `pyinstaller` (standalone binary packaging)
* `github actions` (multi-platform build automation)

---

## 🚀 **AI-Friendly Quality Rules**

* Never suggest a command you are not 100% sure about.
* When you are not sure about the right command, do not pre-write it in the terminal.
* Always code **idempotent and robust**
* No fragile file parsing.
* Clear handling of API errors (timeouts, rate limits, bad responses).
* Systematic validation of user inputs.
* Security by default before executing shell commands.

---

There, with this documentation, any AI (or human dev) can confidently start developing the project.

---

👉 **Do you now want me to move to the next phase and generate for you:**

* The **complete `AskIT-CLI` Starter Kit**
* The **Repo ready to be pushed to GitHub**
* The **GitHub Actions Workflows for multi-platform builds**

You could literally start your first tests this weekend 🎯.

**If you give me the go-ahead, I'll start generating the skeleton.**
