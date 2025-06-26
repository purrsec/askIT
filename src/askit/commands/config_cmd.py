import asyncio
from pathlib import Path
import yaml
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from rich.console import Console

from ..core import project
from ..core.config_manager import (
    get_config_file, 
    get_data_dir, 
    migrate_old_config_if_needed,
    ensure_config_directories
)
from ..security import secrets_manager

console = Console()

def load_config(config_path: Path) -> dict:
    if not config_path.is_file():
        return {"mode": "normal"}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f) or {"mode": "normal"}

def save_config(config_path: Path, config: dict):
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

def create_config_completer():
    """Create autocompletion for the configuration shell."""
    return NestedCompleter.from_nested_dict({
        'set': {
            'mode': {'normal', 'strike'},
            'api_key': None,
        },
        'show': {
            'config': None,
            'running': None,
            'staged': None,
        },
        'commit': None,
        'discard': None,
        'help': None,
        '?': None,
        'exit': None,
        'quit': None,
    })

def show_help():
    """Display help information for the configuration shell."""
    console.print("\n[bold]Available Commands:[/bold]")
    console.print()
    console.print("[bold cyan]Configuration Commands:[/bold cyan]")
    console.print("  [cyan]set mode <value>[/cyan]        Set execution mode (strike|normal)")
    console.print("  [cyan]set api_key[/cyan]             Configure API key (secure input)")
    console.print()
    console.print("[bold cyan]Information Commands:[/bold cyan]")
    console.print("  [cyan]show config[/cyan]             Display current configuration")
    console.print("  [cyan]show running[/cyan]            Display active configuration")
    console.print("  [cyan]show staged[/cyan]             Display pending changes")
    console.print()
    console.print("[bold cyan]Change Management:[/bold cyan]")
    console.print("  [cyan]commit[/cyan]                  Apply staged changes")
    console.print("  [cyan]discard[/cyan]                 Cancel staged changes")
    console.print()
    console.print("[bold cyan]General Commands:[/bold cyan]")
    console.print("  [cyan]help[/cyan] or [cyan]?[/cyan]               Show this help")
    console.print("  [cyan]exit[/cyan] or [cyan]quit[/cyan]            Leave configuration shell")
    console.print()
    console.print("[bold]Execution Modes:[/bold]")
    console.print("  [green]normal[/green]  - Safe mode: shows suggestions without auto-execution")
    console.print("  [yellow]strike[/yellow]  - Fast mode: auto-executes commands when AI is confident")
    console.print()
    console.print("[dim]Note: Changes are staged until you run 'commit' to apply them.[/dim]")
    console.print()

async def config_shell():
    # Ensure configuration directories exist
    ensure_config_directories()
    
    # Try to migrate old config if needed
    migrated = migrate_old_config_if_needed()
    if migrated:
        console.print("[dim]✓ Configuration migrated to OS-standard location[/dim]")
    
    # Use global configuration paths
    config_path = get_config_file()
    data_dir = get_data_dir()
    config_temp_path = data_dir / "config.yaml.tmp"
    config_lock_path = data_dir / ".config.lock"

    running_config = load_config(config_path)
    
    if config_lock_path.exists():
        console.print("[yellow]Uncommitted configuration changes found.[/yellow]")
        staged_config = load_config(config_temp_path)
        # Ensure staged_config has all the keys from running_config if not present
        for key, value in running_config.items():
            if key not in staged_config:
                staged_config[key] = value
    else:
        staged_config = running_config.copy()

    history = FileHistory(data_dir / '.config_history')
    completer = create_config_completer()
    
    # Define styles for the prompt
    style = Style.from_dict({
        'prompt': 'ansicyan',
        'modified': 'ansiyellow bold',
    })
    
    session = PromptSession(
        history=history, 
        completer=completer, 
        complete_while_typing=True,
        style=style
    )

    console.print("[bold cyan]AskIT-CLI Configuration Shell[/bold cyan]")
    console.print("Type [cyan]help[/cyan] or [cyan]?[/cyan] for available commands")
    console.print("[dim]💡 Use [cyan]Tab[/cyan] for autocompletion[/dim]")
    console.print()

    while True:
        try:
            # Dynamic prompt showing staged changes - use FormattedText for proper ANSI handling
            if config_lock_path.exists():
                prompt_text = FormattedText([
                    ('class:prompt', 'askit-config'),
                    ('class:modified', '*'),
                    ('class:prompt', '> ')
                ])
            else:
                prompt_text = FormattedText([
                    ('class:prompt', 'askit-config> ')
                ])
            
            cmd_input = await session.prompt_async(prompt_text)
            parts = cmd_input.strip().split()
            if not parts:
                continue

            command = parts[0].lower()

            # Help commands
            if command in ["help", "?"]:
                show_help()
                continue

            # Exit commands
            elif command in ["exit", "quit"]:
                if config_lock_path.exists():
                    console.print("[yellow]⚠ You have uncommitted changes.[/yellow]")
                    confirm = await session.prompt_async("Exit anyway? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                # Clean up before exiting
                config_temp_path.unlink(missing_ok=True)
                config_lock_path.unlink(missing_ok=True)
                console.print("Configuration shell closed.")
                break
            # Change management commands
            elif command == "commit":
                if not config_lock_path.exists():
                    console.print("[yellow]ⓘ No pending changes to commit.[/yellow]")
                    continue
                
                # Handle API key commit if staged
                if "api_key" in staged_config:
                    api_key = staged_config.pop("api_key")  # Remove from config before saving
                    if secrets_manager.set_api_key(api_key):
                        console.print("[green]✓ API key applied to system keychain.[/green]")
                    else:
                        console.print("[bold red]✗ Failed to store API key in system keychain.[/bold red]")
                        console.print("[dim]   Consider setting the ANTHROPIC_API_KEY environment variable instead.[/dim]")
                        # Re-add to staged config since it failed
                        staged_config["api_key"] = api_key
                        save_config(config_temp_path, staged_config)
                        continue
                
                # Save other configuration changes
                save_config(config_path, staged_config)
                config_temp_path.unlink()
                config_lock_path.unlink()
                running_config = staged_config.copy()
                console.print("[bold green]✓ Configuration committed and applied successfully.[/bold green]")
                
            elif command == "discard":
                if not config_lock_path.exists():
                    console.print("[yellow]ⓘ No pending changes to discard.[/yellow]")
                    continue
                
                # Check what changes are being discarded
                changes_discarded = []
                if staged_config.get("mode") != running_config.get("mode"):
                    changes_discarded.append("mode")
                if "api_key" in staged_config:
                    changes_discarded.append("api_key")
                
                config_temp_path.unlink()
                config_lock_path.unlink()
                staged_config = running_config.copy()
                
                if changes_discarded:
                    console.print(f"[bold yellow]✓ Staged changes discarded:[/bold yellow] {', '.join(changes_discarded)}")
                else:
                    console.print("[bold yellow]✓ Staged changes discarded.[/bold yellow]")

            # Configuration commands
            elif command == "set":
                if len(parts) < 2:
                    console.print("[red]✗ Missing parameter.[/red] Usage: [cyan]set mode <value>[/cyan] or [cyan]set api_key[/cyan]")
                    console.print("   Type [cyan]help[/cyan] for more information.")
                elif parts[1].lower() == "mode":
                    if len(parts) < 3:
                        console.print(f"[red]✗ Missing mode value.[/red] Current mode: [yellow]{running_config.get('mode', 'normal')}[/yellow]")
                        console.print("   Usage: [cyan]set mode <strike|normal>[/cyan]")
                    elif parts[2].lower() not in ["strike", "normal"]:
                        console.print(f"[red]✗ Invalid mode '[yellow]{parts[2]}[/yellow]'.[/red] Valid modes: [green]normal[/green], [yellow]strike[/yellow]")
                    else:
                        old_mode = staged_config.get("mode", "normal")
                        new_mode = parts[2].lower()
                        staged_config["mode"] = new_mode
                        save_config(config_temp_path, staged_config)
                        config_lock_path.touch()
                        if old_mode != new_mode:
                            console.print(f"[green]✓ Mode changed:[/green] [dim]{old_mode}[/dim] → [bold green]{new_mode}[/bold green]")
                            console.print("[dim]   Use [cyan]commit[/cyan] to apply changes.[/dim]")
                        else:
                            console.print(f"[yellow]ⓘ Mode already set to [bold]{new_mode}[/bold].[/yellow]")
                elif parts[1].lower() == "api_key":
                    # Use prompt_toolkit with password input
                    api_key = await session.prompt_async('Enter your API key (input hidden): ', is_password=True)

                    if not api_key.strip():
                        console.print("[yellow]⚠ Empty API key, operation cancelled.[/yellow]")
                    else:
                        # Stage the API key change
                        old_api_status = "present" if secrets_manager.get_api_key() else "missing"
                        staged_config["api_key"] = api_key  # Store temporarily for staging
                        save_config(config_temp_path, staged_config)
                        config_lock_path.touch()
                        console.print(f"[green]✓ API key staged:[/green] [dim]{old_api_status}[/dim] → [bold green]new key[/bold green]")
                        console.print("[dim]   Use [cyan]commit[/cyan] to apply changes.[/dim]")

                        # Re-create the session object to fully reset the terminal state after password input.
                        session = PromptSession(
                            history=history, 
                            completer=completer, 
                            complete_while_typing=True,
                            style=style
                        )
                else:
                    console.print(f"[red]✗ Unknown parameter '[yellow]{parts[1]}[/yellow]'.[/red]")
                    console.print("   Available: [cyan]mode[/cyan], [cyan]api_key[/cyan]")
                    console.print("   Type [cyan]help[/cyan] for detailed usage.")

            # Information commands
            elif command == "show":
                if len(parts) < 2:
                    console.print("[red]✗ Missing show target.[/red] Usage: [cyan]show <config|running|staged>[/cyan]")
                elif parts[1].lower() == "config":
                    # Show complete configuration overview
                    console.print("\n[bold cyan]╭─ Configuration Overview ─╮[/bold cyan]")
                    console.print()
                    console.print("[bold]🔧 Active Configuration:[/bold]")
                    console.print(f"   Mode: [green]{running_config.get('mode', 'normal')}[/green]")
                    
                    api_key = secrets_manager.get_api_key()
                    if api_key:
                        console.print("   API Key: [bold green]✓ Configured[/bold green] (stored in keychain)")
                    else:
                        console.print("   API Key: [bold red]✗ Missing[/bold red]")
                    
                    if config_lock_path.exists():
                        console.print()
                        console.print("[bold yellow]⚠ Pending Changes:[/bold yellow]")
                        if staged_config.get("mode") != running_config.get("mode"):
                            console.print(f"   Mode: [yellow]{staged_config.get('mode', 'normal')}[/yellow] (staged)")
                        if "api_key" in staged_config:
                            console.print("   API Key: [yellow]✓ New key staged[/yellow]")
                        console.print("[dim]   Use [cyan]commit[/cyan] to apply or [cyan]discard[/cyan] to cancel.[/dim]")
                    console.print()
                    
                elif parts[1].lower() == "running":
                    # Show only active configuration
                    console.print("\n[bold green]Active Configuration:[/bold green]")
                    console.print(f"  Mode: [green]{running_config.get('mode', 'normal')}[/green]")
                    api_key = secrets_manager.get_api_key()
                    if api_key:
                        console.print("  API Key: [bold green]✓ Present[/bold green]")
                    else:
                        console.print("  API Key: [bold red]✗ Missing[/bold red]")
                    console.print()
                    
                elif parts[1].lower() == "staged":
                    # Show staged changes
                    if not config_lock_path.exists():
                        console.print("[yellow]ⓘ No staged changes.[/yellow]")
                    else:
                        console.print("\n[bold yellow]Staged Changes:[/bold yellow]")
                        changes_found = False
                        if staged_config.get("mode") != running_config.get("mode"):
                            console.print(f"  Mode: [yellow]{staged_config.get('mode', 'normal')}[/yellow]")
                            changes_found = True
                        if "api_key" in staged_config:
                            console.print("  API Key: [yellow]✓ New key staged[/yellow]")
                            changes_found = True
                        
                        if changes_found:
                            console.print("[dim]  Use [cyan]commit[/cyan] to apply these changes.[/dim]")
                        else:
                            console.print("[dim]  No changes detected.[/dim]")
                    console.print()
                else:
                    console.print(f"[red]✗ Unknown show target '[yellow]{parts[1]}[/yellow]'.[/red]")
                    console.print("   Available: [cyan]config[/cyan], [cyan]running[/cyan], [cyan]staged[/cyan]")
                    
            else:
                console.print(f"[red]✗ Unknown command '[yellow]{cmd_input}[/yellow]'.[/red]")
                console.print("   Type [cyan]help[/cyan] or [cyan]?[/cyan] for available commands.")

        except (EOFError, KeyboardInterrupt):
            # Force cleanup on Ctrl+C / Ctrl+D
            console.print("\n[yellow]⚠ Interrupted by user.[/yellow]")
            if config_lock_path.exists():
                console.print("[dim]Uncommitted changes discarded.[/dim]")
            config_temp_path.unlink(missing_ok=True)
            config_lock_path.unlink(missing_ok=True)
            break

    console.print("[dim]Configuration shell closed.[/dim]") 