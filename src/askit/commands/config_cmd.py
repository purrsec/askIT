import asyncio
from pathlib import Path
import yaml
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console

from ..core import project
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

async def config_shell():
    project_root = project.find_project_root()
    if not project_root:
        console.print("[bold red]Error:[/bold red] You are not in an AskIT project. Run `askit-cli init` first.")
        return

    askit_dir = project_root / ".askit"
    config_path = askit_dir / "config.yaml"
    config_temp_path = askit_dir / "config.yaml.tmp"
    config_lock_path = askit_dir / ".config.lock"

    running_config = load_config(config_path)
    
    if config_lock_path.exists():
        console.print("[yellow]Uncommitted configuration changes found.[/yellow]")
        staged_config = load_config(config_temp_path)
    else:
        staged_config = running_config.copy()

    history = FileHistory(askit_dir / '.config_history')
    session = PromptSession(history=history)

    console.print("Welcome to the AskIT-CLI configuration shell.")
    console.print("Commands: `set`, `show config`, `commit`, `discard`, `exit`")

    while True:
        try:
            prompt_char = 'askit-config*>' if config_lock_path.exists() else 'askit-config> '
            cmd_input = await session.prompt_async(prompt_char)
            parts = cmd_input.strip().split()
            if not parts:
                continue

            command = parts[0].lower()

            if command == "exit":
                if config_lock_path.exists():
                    confirm = await session.prompt_async("Uncommitted changes will be lost. Exit anyway? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                # Clean up before exiting
                config_temp_path.unlink(missing_ok=True)
                config_lock_path.unlink(missing_ok=True)
                break
            elif command == "commit":
                if not config_lock_path.exists():
                    console.print("[yellow]No changes to commit.[/yellow]")
                    continue
                save_config(config_path, staged_config)
                config_temp_path.unlink()
                config_lock_path.unlink()
                running_config = staged_config.copy()
                console.print("[bold green]Configuration committed and applied.[/bold green]")
            elif command == "discard":
                if not config_lock_path.exists():
                    console.print("[yellow]No changes to discard.[/yellow]")
                    continue
                config_temp_path.unlink()
                config_lock_path.unlink()
                staged_config = running_config.copy()
                console.print("[bold yellow]Changes discarded.[/bold yellow]")

            elif command == "set":
                if len(parts) >= 3 and parts[1].lower() == "mode" and parts[2].lower() in ["strike", "normal"]:
                    staged_config["mode"] = parts[2].lower()
                    save_config(config_temp_path, staged_config)
                    config_lock_path.touch()
                    console.print(f"Staged mode: [bold green]{staged_config['mode']}[/bold green]. Use `commit` to apply.")
                elif len(parts) >= 2 and parts[1].lower() == "api_key":
                    api_key = await session.prompt_async('Enter your API key (hidden): ', is_password=True)
                    if secrets_manager.set_api_key(api_key):
                        console.print("[bold green]API key stored successfully in the OS keychain (immediately active).[/bold green]")
                    else:
                        console.print("[bold red]Error:[/bold red] Could not store API key. No system keychain found.")
                else:
                    console.print(f"[bold red]Invalid or incomplete 'set' command.[/bold red]")

            elif command == "show" and len(parts) > 1 and parts[1].lower() == "config":
                console.print("\n[bold]Running Configuration:[/bold]")
                console.print(f"  - Mode: {running_config.get('mode', 'normal')}")
                
                if config_lock_path.exists():
                    console.print("\n[bold yellow]Staged Changes (not applied):[/bold yellow]")
                    console.print(f"  - Mode: {staged_config.get('mode', 'normal')}")

                api_key = secrets_manager.get_api_key()
                if api_key:
                    console.print("\n  - API Key: [bold green]Present[/bold green] (stored in keychain)")
                else:
                    console.print("\n  - API Key: [bold red]Missing[/bold red]")
            else:
                console.print(f"[bold red]Unknown command:[/bold red] {cmd_input}")

        except (EOFError, KeyboardInterrupt):
            # Force cleanup on Ctrl+C / Ctrl+D
            config_temp_path.unlink(missing_ok=True)
            config_lock_path.unlink(missing_ok=True)
            break

    console.print("Goodbye!") 