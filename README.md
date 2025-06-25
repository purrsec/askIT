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

### 1. Download and Install

**Windows:**
1. Go to [Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-windows-x86_64.zip`
3. Extract to `C:\Program Files\AskIT\`
4. Add `C:\Program Files\AskIT\` to your PATH environment variable
5. Restart your terminal

**macOS:**
1. Go to [Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-macos-arm64.pkg`
3. Double-click the `.pkg` file and follow the installer
4. Or see [INSTALL.md](INSTALL.md) for manual installation

**Linux (Debian/Ubuntu):**
1. Go to [Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-linux-amd64.deb`
3. Install with: `sudo dpkg -i askit-cli-v0.1.0-linux-amd64.deb`
4. Fix dependencies if needed: `sudo apt-get install -f`

### 2. Configure API Key

Run the configuration wizard:
```bash
askit-cli config
```

### 3. Start Asking!

```bash
# Basic usage
askit-cli -p "list all docker containers"
askit-cli -p "find large files in this directory"
askit-cli -p "check disk usage and show top directories"

# With context (uses more shell history)
askit-cli -c 20 -p "restart the web server from my last session"

# Safe mode (won't execute, just shows commands)
askit-cli --safe -p "delete all log files older than 30 days"
```

## 📋 Installation Troubleshooting

### Windows Security Warning

If you see "Windows protected your PC" warning:

1. Click **"More info"**
2. Click **"Run anyway"**
3. Or disable Windows Defender SmartScreen temporarily

**Alternative**: Use Windows Subsystem for Linux (WSL) and follow Linux instructions.

### macOS Security Issues

If you see "cannot be opened because the developer cannot be verified":

```bash
# Method 1: Allow the specific app
sudo xattr -rd com.apple.quarantine /usr/local/lib/askit-cli/
sudo spctl --add /usr/local/lib/askit-cli/askit-cli

# Method 2: Temporarily disable Gatekeeper (not recommended)
sudo spctl --master-disable
# Re-enable after installation
sudo spctl --master-enable
```

### Linux Permission Issues

If you get permission errors:
```bash
# Fix permissions
sudo chmod +x /usr/local/bin/askit-cli
sudo chmod +x /usr/local/lib/askit-cli/askit-cli

# Or install to user directory
mkdir -p ~/.local/bin
cp askit-cli ~/.local/bin/
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

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