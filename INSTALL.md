# 📦 Installation Guide

This guide provides detailed installation instructions for AskIT CLI across all supported platforms, including solutions for common security and certificate issues.

## 🚀 Manual Installation

### Windows

**Step-by-step installation:**
1. Go to [GitHub Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-windows-x86_64.zip`
3. Extract the ZIP file to `C:\Program Files\AskIT\`
4. Add `C:\Program Files\AskIT\` to your PATH:
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add `C:\Program Files\AskIT`
   - Click "OK" to save
5. Restart your terminal/command prompt
6. Test: `askit-cli --version`

**Alternative: User-only installation**
1. Extract to `%USERPROFILE%\AppData\Local\AskIT\` instead
2. Add that path to your user PATH (not system PATH)

### macOS

**Step-by-step installation:**
1. Go to [GitHub Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-macos-arm64.pkg`
3. Double-click the `.pkg` file to run the installer
4. Follow the installation wizard
5. Open Terminal and test: `askit-cli --version`

**Manual installation (if pkg doesn't work):**
1. Download the `.pkg` file
2. Right-click and select "Open" (may need to bypass security warnings)
3. Or extract manually and copy files to `/usr/local/bin/` and `/usr/local/lib/`

### Linux

**Debian/Ubuntu (.deb package):**
1. Go to [GitHub Releases](https://github.com/purrsec/askIT/releases/latest)
2. Download `askit-cli-v0.1.0-linux-amd64.deb`
3. Install: `sudo dpkg -i askit-cli-v0.1.0-linux-amd64.deb`
4. Fix dependencies if needed: `sudo apt-get install -f`
5. Test: `askit-cli --version`

**Red Hat/CentOS/Fedora:**
1. Download the `.deb` file (no .rpm yet available)
2. Convert using alien: `sudo dnf install alien && sudo alien -r askit-cli-*.deb`
3. Install: `sudo rpm -i askit-cli-*.rpm`

**Manual installation (any Linux):**
1. Download the `.deb` file
2. Extract: `ar x askit-cli-*.deb && tar xf data.tar.xz`
3. Copy files:
   - `sudo cp usr/local/bin/askit-cli /usr/local/bin/`
   - `sudo cp -r usr/local/lib/askit-cli /usr/local/lib/`
4. Make executable: `sudo chmod +x /usr/local/bin/askit-cli`
5. Test: `askit-cli --version`

## 🛡️ Security & Certificate Issues

### Windows Security Warnings

#### Issue: "Windows protected your PC" SmartScreen Warning

**Solution 1: Allow this specific app**
1. When the warning appears, click **"More info"**
2. Click **"Run anyway"**
3. The app will be remembered as safe

**Solution 2: Disable SmartScreen temporarily**
```powershell
# Disable SmartScreen (requires Admin)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"

# Re-enable after installation
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "RequireAdmin"
```

**Solution 3: Use Windows Subsystem for Linux (WSL)**
```powershell
# Install WSL if not already installed
wsl --install

# Then follow Linux installation instructions inside WSL
wsl
```

#### Issue: Antivirus False Positives

Some antivirus programs may flag PyInstaller executables as suspicious.

**Temporary whitelist:**
```powershell
# Windows Defender
Add-MpPreference -ExclusionPath "$env:ProgramFiles\AskIT"

# For other antivirus software, add the installation directory to exclusions
```

### macOS Security Issues

#### Issue: "cannot be opened because the developer cannot be verified"

This happens because our binaries are not code-signed with an Apple Developer certificate.

**Solution 1: Allow specific application (Recommended)**
```bash
# Remove quarantine attribute
sudo xattr -rd com.apple.quarantine /usr/local/lib/askit-cli/

# Add to Gatekeeper allowlist
sudo spctl --add /usr/local/lib/askit-cli/askit-cli
sudo spctl --enable /usr/local/lib/askit-cli/askit-cli
```

**Solution 2: Temporary Gatekeeper disable (Not recommended)**
```bash
# Disable Gatekeeper temporarily
sudo spctl --master-disable

# Install AskIT CLI
sudo installer -pkg askit-cli.pkg -target /

# Re-enable Gatekeeper
sudo spctl --master-enable
```

**Solution 3: Manual permission grant**
1. Try to run `askit-cli` in Terminal
2. Go to **System Preferences** → **Security & Privacy** → **General**
3. Click **"Allow Anyway"** next to the blocked app message
4. Try running again and click **"Open"** when prompted

#### Issue: Permission Denied Errors

```bash
# Fix executable permissions
sudo chmod +x /usr/local/bin/askit-cli
sudo chmod +x /usr/local/lib/askit-cli/askit-cli

# Fix ownership if needed
sudo chown -R $(whoami):staff /usr/local/lib/askit-cli/
```

### Linux Security Issues

#### Issue: Permission Denied

```bash
# Fix permissions
sudo chmod +x /usr/local/bin/askit-cli
sudo chmod +x /usr/local/lib/askit-cli/askit-cli

# If still issues, check SELinux context
sudo restorecon -v /usr/local/bin/askit-cli
sudo restorecon -Rv /usr/local/lib/askit-cli/
```

#### Issue: Missing Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -f
sudo apt-get install libc6 libssl3

# CentOS/RHEL/Fedora
sudo dnf install glibc openssl-libs

# Alpine Linux
sudo apk add glibc libssl1.1
```

#### Issue: AppArmor/SELinux Restrictions

```bash
# Check if AppArmor is blocking
sudo dmesg | grep -i apparmor | grep askit

# If blocked, create an AppArmor profile or disable for this app
sudo aa-complain /usr/local/bin/askit-cli

# For SELinux
sudo setsebool -P allow_execstack 1
```

## 🔧 Advanced Installation Options

### Development Installation

For developers who want to run from source:

```bash
# Clone the repository
git clone https://github.com/purrsec/askIT.git
cd askIT

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run from source
poetry run python run_cli.py --help
```

### Custom Installation Directory

**Windows:**
1. Extract the ZIP file to your preferred directory (e.g., `C:\Tools\AskIT\`)
2. Add that directory to your user PATH:
   - Open Settings → Search for "environment"
   - Click "Edit environment variables for your account"
   - Add your custom path to the user PATH variable

**Linux/macOS:**
1. Extract or copy files to `~/.local/bin/` and `~/.local/lib/askit-cli/`
2. Add to your shell configuration:
   - `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc`
   - `source ~/.bashrc`

### Docker Installation

For isolated environments:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y wget
RUN wget "https://github.com/purrsec/askIT/releases/latest/download/askit-cli-v0.1.0-linux-amd64.deb"
RUN dpkg -i askit-cli-v0.1.0-linux-amd64.deb

ENTRYPOINT ["askit-cli"]
```

```bash
# Build and run
docker build -t askit-cli .
docker run -it --rm askit-cli --help
```

## ✅ Verification

After installation, verify everything works:

```bash
# Check version
askit-cli --version

# Check configuration
askit-cli config

# Test basic functionality
askit-cli --safe -p "show current directory contents"
```

## 🆘 Troubleshooting

### Common Issues

**"Command not found"**
- Verify PATH is correctly set
- Restart your terminal
- Check if the binary has execute permissions

**"Permission denied"**
- Run `chmod +x` on the binary
- Check if antivirus is blocking execution
- Verify you have sufficient privileges

**"SSL/TLS errors"**
- Update your system's CA certificates
- Check internet connectivity
- Verify proxy settings if behind corporate firewall

**API Key issues**
- Run `askit-cli config` to set up your Anthropic API key
- Verify the key is valid at https://console.anthropic.com
- Check that keyring service is available on your system

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues**: [GitHub Issues](https://github.com/purrsec/askIT/issues)
2. **Create a new issue**: Include your OS, version, and error messages
3. **Join discussions**: [GitHub Discussions](https://github.com/purrsec/askIT/discussions)
4. **Security issues**: Email git.lpl@protonmail.com

---

**Next step**: After installation, run `askit-cli config` to set up your API key and start using AskIT CLI! 