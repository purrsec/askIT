"""
Configuration manager for askit-cli.
Handles proper configuration file placement according to OS conventions.
"""
import os
import platform
from pathlib import Path
from typing import Optional


def get_config_dir() -> Path:
    """
    Get the appropriate configuration directory for the current OS.
    
    Returns the path to the configuration directory, creating it if necessary.
    
    OS-specific locations:
    - macOS (Darwin): ~/Library/Application Support/askit-cli/
    - Linux: ~/.config/askit-cli/ (or $XDG_CONFIG_HOME/askit-cli/)
    - Windows: %APPDATA%/askit-cli/
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "askit-cli"
    elif system == "Linux":
        # Respect XDG Base Directory Specification
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_dir = Path(xdg_config_home) / "askit-cli"
        else:
            config_dir = Path.home() / ".config" / "askit-cli"
    elif system == "Windows":
        # Use APPDATA for user-specific configuration
        appdata = os.environ.get("APPDATA")
        if appdata:
            config_dir = Path(appdata) / "askit-cli"
        else:
            # Fallback to user profile
            config_dir = Path.home() / "AppData" / "Roaming" / "askit-cli"
    else:
        # Fallback for unknown systems
        config_dir = Path.home() / ".askit-cli"
    
    # Create the directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    return config_dir


def get_config_file() -> Path:
    """
    Get the path to the main configuration file.
    
    Returns the path to config.yaml in the OS-appropriate config directory.
    """
    return get_config_dir() / "config.yaml"


def get_cache_dir() -> Path:
    """
    Get the appropriate cache directory for the current OS.
    
    OS-specific locations:
    - macOS (Darwin): ~/Library/Caches/askit-cli/
    - Linux: ~/.cache/askit-cli/ (or $XDG_CACHE_HOME/askit-cli/)
    - Windows: %LOCALAPPDATA%/askit-cli/cache/
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        cache_dir = Path.home() / "Library" / "Caches" / "askit-cli"
    elif system == "Linux":
        # Respect XDG Base Directory Specification
        xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
        if xdg_cache_home:
            cache_dir = Path(xdg_cache_home) / "askit-cli"
        else:
            cache_dir = Path.home() / ".cache" / "askit-cli"
    elif system == "Windows":
        # Use LOCALAPPDATA for cache data
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata:
            cache_dir = Path(localappdata) / "askit-cli" / "cache"
        else:
            # Fallback to user profile
            cache_dir = Path.home() / "AppData" / "Local" / "askit-cli" / "cache"
    else:
        # Fallback for unknown systems
        cache_dir = Path.home() / ".askit-cli" / "cache"
    
    # Create the directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return cache_dir


def get_data_dir() -> Path:
    """
    Get the appropriate data directory for the current OS.
    
    OS-specific locations:
    - macOS (Darwin): ~/Library/Application Support/askit-cli/
    - Linux: ~/.local/share/askit-cli/ (or $XDG_DATA_HOME/askit-cli/)
    - Windows: %APPDATA%/askit-cli/data/
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # On macOS, data and config are often in the same location
        data_dir = Path.home() / "Library" / "Application Support" / "askit-cli"
    elif system == "Linux":
        # Respect XDG Base Directory Specification
        xdg_data_home = os.environ.get("XDG_DATA_HOME")
        if xdg_data_home:
            data_dir = Path(xdg_data_home) / "askit-cli"
        else:
            data_dir = Path.home() / ".local" / "share" / "askit-cli"
    elif system == "Windows":
        # Use APPDATA for data
        appdata = os.environ.get("APPDATA")
        if appdata:
            data_dir = Path(appdata) / "askit-cli" / "data"
        else:
            # Fallback to user profile
            data_dir = Path.home() / "AppData" / "Roaming" / "askit-cli" / "data"
    else:
        # Fallback for unknown systems
        data_dir = Path.home() / ".askit-cli" / "data"
    
    # Create the directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir


def get_logs_dir() -> Path:
    """
    Get the appropriate logs directory for the current OS.
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        logs_dir = Path.home() / "Library" / "Logs" / "askit-cli"
    elif system == "Linux":
        # On Linux, logs often go in a subdirectory of data or cache
        logs_dir = get_cache_dir() / "logs"
    elif system == "Windows":
        # Use LOCALAPPDATA for logs
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata:
            logs_dir = Path(localappdata) / "askit-cli" / "logs"
        else:
            logs_dir = Path.home() / "AppData" / "Local" / "askit-cli" / "logs"
    else:
        # Fallback for unknown systems
        logs_dir = Path.home() / ".askit-cli" / "logs"
    
    # Create the directory if it doesn't exist
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    return logs_dir


def get_project_context_file(project_root: Path) -> Path:
    """
    Get the path to the project-specific context file.
    
    This is still stored in the project's .askit directory for project-specific context.
    """
    return project_root / ".askit" / "context.json"


def get_project_config_file(project_root: Path) -> Path:
    """
    Get the path to the project-specific configuration file.
    
    This is stored in the project's .askit directory for project-specific settings.
    """
    return project_root / ".askit" / "config.yaml"


def migrate_old_config_if_needed() -> bool:
    """
    Migrate configuration from old .askit/config.yaml to new OS-appropriate location.
    
    Returns True if migration was performed, False otherwise.
    """
    # Check if we're in a project with old config
    from .project import find_project_root
    
    project_root = find_project_root()
    if not project_root:
        return False
    
    old_config_file = project_root / ".askit" / "config.yaml"
    new_config_file = get_config_file()
    
    # If old config exists and new config doesn't exist, migrate
    if old_config_file.exists() and not new_config_file.exists():
        try:
            import shutil
            shutil.copy2(old_config_file, new_config_file)
            
            # Leave a note in the old location
            migration_note = project_root / ".askit" / "config_migrated.txt"
            migration_note.write_text(
                f"Configuration has been migrated to: {new_config_file}\n"
                f"This is the new standard location for askit-cli configuration.\n"
            )
            
            return True
        except Exception:
            return False
    
    return False


def ensure_config_directories():
    """
    Ensure all necessary configuration directories exist.
    """
    get_config_dir()
    get_cache_dir()
    get_data_dir()
    get_logs_dir() 