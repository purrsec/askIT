# AskIT CLI

![](https://img.shields.io/badge/Python-3.12%2B-brightgreen?style=flat-square) 
![](https://img.shields.io/github/v/release/purrsec/askIT?style=flat-square) 
![](https://img.shields.io/github/license/purrsec/askIT?style=flat-square)

🔧 **Claude-powered CLI for SysAdmins, SecOps, and DevOps.** Ask questions in natural language and get instant shell commands with explanations. Like having Claude in your terminal.

AskIT CLI is an intelligent command-line assistant that understands your system context, analyzes your shell history, and provides tailored command suggestions through natural language queries. Use it to automate routine tasks, explain complex commands, and accelerate your workflow -- all through simple English questions.

## ✨ Features

- 🤖 **AI-Powered Suggestions**: Leverages Claude AI for intelligent command generation
- 📚 **Context Awareness**: Analyzes shell history and detects project types
- ⚡ **Multiple Execution Modes**: Normal, Strike (auto-execute), and Safe modes
- 🛡️ **Security First**: Built-in safe mode and command validation
- 🔄 **Interactive Workflows**: Ask follow-up questions for complex tasks
- 🎯 **Smart Configuration**: Auto-detects shell and installs tab completion
- 📦 **Cross-Platform**: Available as native binaries for Windows, macOS, and Linux

## 🚀 Quick Start



## 🎯 Usage Examples

### System Administration
```bash
askit-cli -p "show me all processes using more than 100MB RAM"
askit-cli -p "check if port 443 is open and what's using it"
askit-cli -p "create a backup of /etc/nginx/nginx.conf"
```

### Security Operations
```bash
askit-cli -p "show failed login attempts from the last hour"
askit-cli -p "check for unusual network connections"
askit-cli -p "scan for files with SUID bit set"
```

### DevOps Tasks
```bash
askit-cli -p "deploy the latest version to staging"
askit-cli -p "check the health of all kubernetes pods"
askit-cli -p "rotate the application logs"
```

## ⚙️ Configuration

AskIT CLI supports multiple configuration options:

### Execution Modes
- **Normal**: Shows command and explanation (default)
- **Strike**: Auto-executes high-confidence commands
- **Safe**: Never executes, only shows suggestions

### Shell Integration
AskIT automatically installs tab completion for your shell (bash, zsh, fish).

### Project Detection
Automatically detects and provides context for:
- Git repositories
- Docker projects
- Node.js applications
- Python projects
- And more...

## 🔒 Privacy and Security

### Data Collection
- We collect minimal usage data to improve the service
- No sensitive data or credentials are stored
- All data is encrypted in transit and at rest

### API Key Security
- Your Anthropic API key is stored securely using your system's keyring
- Keys are never transmitted except to Anthropic's official API endpoints

### Safe Mode
Use `--safe` flag to preview commands without execution:
```bash
askit-cli --safe -p "your potentially dangerous command"
```

## 🐛 Reporting Issues

Found a bug or have a suggestion? 

1. **GitHub Issues**: [File an issue](https://github.com/purrsec/askIT/issues)
2. **Security Issues**: Email git.lpl@protonmail.com
3. **General Questions**: Start a [Discussion](https://github.com/purrsec/askIT/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**⚠️ Important**: AskIT CLI is a powerful tool that can execute system commands. Always review suggestions before execution, especially in production environments. Use `--safe` mode when in doubt.