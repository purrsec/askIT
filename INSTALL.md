# 📦 Installation Guide

This guide provides detailed installation instructions for AskIT CLI across all supported platforms, including solutions for common security and certificate issues.

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
askit-cli -p list all docker containers
askit-cli -p find large files in this directory
askit-cli -p check disk usage and show top directories

# With context (uses more shell history)
askit-cli -c 20 -p restart the web server from my last session

# Safe mode (won't execute, just shows commands)
askit-cli --safe -p delete all log files older than 30 days
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
