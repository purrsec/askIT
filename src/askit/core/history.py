import os
import platform
from pathlib import Path
from typing import List, Optional


def get_shell_history(max_lines: int = 10, debug: bool = False) -> List[str]:
    """
    Retrieve the shell history from the current user's shell.
    
    Args:
        max_lines: Maximum number of history lines to retrieve
        debug: Whether to print debug information
        
    Returns:
        List of command history lines, most recent first
    """
    try:
        system = platform.system()
        history_lines = []
        
        if debug:
            print(f"[DEBUG] System: {system}")
            print(f"[DEBUG] Shell env: {os.environ.get('SHELL', 'Not set')}")
        
        # Fetch more lines to have enough after filtering
        fetch_lines = max_lines * 2 
        
        if system == "Windows":
            history_lines = _get_powershell_history(fetch_lines, debug)
        else:
            # Linux/macOS
            history_lines = _get_unix_shell_history(fetch_lines, debug)

        # Filter out askit-cli commands from history
        filtered_history = [
            line for line in history_lines 
            if "askit-cli" not in line.strip()
        ]
            
        if debug:
            print(f"[DEBUG] Retrieved {len(history_lines)} history lines")
            print(f"[DEBUG] Filtered to {len(filtered_history)} lines")
            
        return filtered_history[:max_lines] if filtered_history else []
    except Exception as e:
        if debug:
            print(f"[DEBUG] Exception in get_shell_history: {e}")
        # If we can't get history for any reason, return empty list
        return []


def _get_powershell_history(max_lines: int, debug: bool = False) -> List[str]:
    """Get PowerShell history on Windows."""
    try:
        import subprocess
        
        # Try multiple approaches for PowerShell history
        
        # Method 1: Use Get-History (current session)
        if debug:
            print("[DEBUG] Trying Get-History (current session)")
        
        cmd = ["powershell", "-Command", f"Get-History | Select-Object -Last {max_lines} | ForEach-Object {{ $_.CommandLine }}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if debug:
            print(f"[DEBUG] Get-History result code: {result.returncode}")
            print(f"[DEBUG] Get-History stdout: '{result.stdout.strip()}'")
            print(f"[DEBUG] Get-History stderr: '{result.stderr.strip()}'")
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            if lines:
                return list(reversed(lines))
        
        # Method 2: Try reading PowerShell history file
        if debug:
            print("[DEBUG] Trying PowerShell history file")
            
        history_file = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "PowerShell" / "PSReadLine" / "ConsoleHost_history.txt"
        
        if debug:
            print(f"[DEBUG] Looking for history file: {history_file}")
            print(f"[DEBUG] History file exists: {history_file.exists()}")
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    lines = [line.strip() for line in lines if line.strip()]
                    lines = lines[-max_lines:] if len(lines) > max_lines else lines
                    if lines:
                        return list(reversed(lines))
            except Exception as e:
                if debug:
                    print(f"[DEBUG] Error reading history file: {e}")
        
        # Method 3: Try pwsh (PowerShell Core) if available
        if debug:
            print("[DEBUG] Trying pwsh (PowerShell Core)")
            
        cmd = ["pwsh", "-Command", f"Get-History | Select-Object -Last {max_lines} | ForEach-Object {{ $_.CommandLine }}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if debug:
            print(f"[DEBUG] pwsh result code: {result.returncode}")
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            if lines:
                return list(reversed(lines))
                
    except Exception as e:
        if debug:
            print(f"[DEBUG] Exception in _get_powershell_history: {e}")
    
    return []


def _get_unix_shell_history(max_lines: int, debug: bool = False) -> List[str]:
    """Get shell history on Unix-like systems (Linux/macOS)."""
    history_files = []
    
    # Try to detect shell and get appropriate history file
    shell = os.environ.get('SHELL', '').lower()
    
    if 'bash' in shell:
        history_files = [Path.home() / '.bash_history']
    elif 'zsh' in shell:
        history_files = [Path.home() / '.zsh_history', Path.home() / '.histfile']
    elif 'fish' in shell:
        history_files = [Path.home() / '.local' / 'share' / 'fish' / 'fish_history']
    else:
        # Try common history files
        history_files = [
            Path.home() / '.bash_history',
            Path.home() / '.zsh_history',
            Path.home() / '.histfile',
            Path.home() / '.history'
        ]
    
    # Try to read from history files
    for history_file in history_files:
        if history_file.exists():
            try:
                lines = []
                with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if 'fish' in str(history_file):
                    # Fish history format is different
                    lines = _parse_fish_history(content, max_lines)
                elif 'zsh' in str(history_file):
                    # Zsh extended history format
                    lines = _parse_zsh_history(content, max_lines)
                else:
                    # Simple bash format
                    lines = content.strip().split('\n')
                    lines = [line.strip() for line in lines if line.strip()]
                    lines = lines[-max_lines:] if len(lines) > max_lines else lines
                
                if lines:
                    return list(reversed(lines))  # Most recent first
            except Exception:
                continue
    
    return []


def _parse_fish_history(content: str, max_lines: int) -> List[str]:
    """Parse fish shell history format."""
    lines = []
    current_cmd = ""
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- cmd:'):
            if current_cmd:
                lines.append(current_cmd)
            current_cmd = line[6:].strip()  # Remove '- cmd: '
        elif line.startswith('  when:') or line.startswith('  paths:'):
            # Skip metadata lines
            continue
        elif current_cmd and line:
            # Multi-line command
            current_cmd += ' ' + line
    
    if current_cmd:
        lines.append(current_cmd)
    
    return lines[-max_lines:] if len(lines) > max_lines else lines


def _parse_zsh_history(content: str, max_lines: int) -> List[str]:
    """Parse zsh extended history format."""
    lines = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Zsh extended history format: : timestamp:elapsed;command
        if line.startswith(':') and ';' in line:
            cmd = line.split(';', 1)[1] if ';' in line else line
            lines.append(cmd.strip())
        else:
            # Simple format
            lines.append(line)
    
    return lines[-max_lines:] if len(lines) > max_lines else lines


def format_history_context(history_lines: List[str]) -> str:
    """
    Format shell history for AI context.
    
    Args:
        history_lines: List of command history lines
        
    Returns:
        Formatted string for AI context
    """
    if not history_lines:
        return "No recent shell history available."
    
    formatted_lines = []
    for i, cmd in enumerate(history_lines, 1):
        # Truncate very long commands
        if len(cmd) > 100:
            cmd = cmd[:97] + "..."
        formatted_lines.append(f"{i:2d}. {cmd}")
    
    return "\n".join(formatted_lines) 