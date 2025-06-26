# 📦 Installation Guide

This guide provides detailed installation instructions for AskIT CLI on all supported platforms, with solutions for common security and certificate issues.

## 🖥️ Platform Installation

### Windows 10/11

1. Download from [Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-windows-x86_64.zip`
3. **Extraction**: Right-click → "Extract all..." to `C:\Program Files\AskIT\`
   - If you don't have permissions, use `%USERPROFILE%\AskIT\` instead
4. **Add to PATH**:
   - Type `sysdm.cpl` in the Start menu
   - "Advanced" tab → "Environment Variables"
   - In "User variables", select "Path" → "Edit"
   - "New" → Add the installation path
   - **Restart your terminal** (PowerShell/CMD)

**🛡️ Windows Security Warning:**
If Windows Defender blocks execution:
1. Click **"More info"**
2. Click **"Run anyway"**
3. **Why?** The application doesn't have a valid code-signing certificate (high cost for an open-source project)

**WSL Alternative:**
If restrictions are too strict, use Windows Subsystem for Linux and follow the Linux instructions.

### macOS (Intel & Apple Silicon)

1. Download from [Releases](https://github.com/purrsec/askIT/releases/)
2. Download:
   - `askit-cli-v0.1.0-macos-arm64.pkg` (Apple Silicon M1/M2/M3)

**📦 PKG Installation (Recommended):**
1. **Double-click** on the `.pkg` file
2. If the error "cannot be opened because the developer cannot be verified" appears:
   - **Right-click** on the `.pkg` file
   - Select **"Open"**
   - Confirm with **"Open"** in the popup
3. Follow the installation wizard

**🔧 Manual Installation (Alternative):**
```bash
# If PKG installation fails
sudo installer -pkg askit-cli-v0.1.0-macos-arm64.pkg -target /

# Or manual extraction
mkdir -p /usr/local/bin
sudo cp askit-cli /usr/local/bin/
sudo chmod +x /usr/local/bin/askit-cli
```

**🔒 Gatekeeper Security Issues:**
```bash
# Method 1: Allow specific application (Recommended)
sudo xattr -rd com.apple.quarantine /usr/local/bin/askit-cli
sudo spctl --add /usr/local/bin/askit-cli

# Method 2: If app is in a folder
sudo xattr -rd com.apple.quarantine /usr/local/lib/askit-cli/
sudo spctl --add /usr/local/lib/askit-cli/askit-cli

# Verification
spctl -a -t exec -vv /usr/local/bin/askit-cli
```

### Linux (Debian/Ubuntu/Mint)

**📦 DEB Installation (Recommended):**

Download the latest version from releases: https://github.com/purrsec/askIT/releases/

Or via command line:
```bash
# Download
wget https://github.com/purrsec/askIT/releases/latest/download/askit-cli-v0.1.0-linux-amd64.deb
```

```bash
# Installation
sudo dpkg -i askit-cli-v0.1.0-linux-amd64.deb

# Resolve dependencies if necessary
sudo apt-get install -f
```

**🐧 Linux Specifics:**
- **AppImage:** Download and make executable with `chmod +x`
- **Permissions:** Ensure `/usr/local/bin` is in your `$PATH`

## ⚙️ Initial Configuration

### 1. API Key Configuration

```bash
# Launch configuration assistant
askit-cli config

# Manual configuration (optional)
export ANTHROPIC_API_KEY="your-key-here"
```

### 2. Installation Verification

```bash
# Basic test
askit-cli --version

# Test with a simple command
askit-cli -p show current directory
```

## 🚀 Getting Started

```bash
# Basic usage
askit-cli -p list all docker containers
askit-cli -p find large files in this directory
askit-cli -p check disk usage and show top directories

# With context (uses more shell history)
askit-cli -c 20 -p restart the web server from my last session

# Safe mode (doesn't execute, just shows commands)
askit-cli --safe -p delete all log files older than 30 days
```

## 🔧 Troubleshooting

### PATH Issues
```bash
# Check if askit-cli is found
which askit-cli

# Add manually to PATH (temporary)
export PATH=$PATH:/usr/local/bin

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
```

### Permission Errors
```bash
# Linux/macOS: Fix permissions
sudo chmod +x /usr/local/bin/askit-cli

# Windows: Check that user has execution rights
icacls "C:\Program Files\AskIT\askit-cli.exe" /grant Users:RX
```

### Certificate/Proxy Issues
```bash
# If you're behind a corporate proxy
export HTTPS_PROXY=http://your-proxy:port
export HTTP_PROXY=http://your-proxy:port

# Ignore SSL certificates (not recommended)
export PYTHONHTTPSVERIFY=0
```

## 📝 Important Notes

- **Security**: The application requires network permissions for the Claude API
- **Updates**: Regularly check for new versions on GitHub
- **Support**: Open a GitHub issue for problems
