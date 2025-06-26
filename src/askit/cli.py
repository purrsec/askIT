import typer
from rich.console import Console
import asyncio
from typing_extensions import Annotated
import sys
import os
from typing import Optional
from rich.prompt import Prompt
from .agent.runtime import run_agent

from ._version import __version__
from .commands.init_cmd import init_project
from .commands.config_cmd import config_shell
from .core import project
from .security import secrets_manager
from .providers.claude import ClaudeProvider
import platform

def show_help():
    """
    Custom help display function that works around Typer's context issues.
    """
    console = Console()
    
    console.print("\n[bold cyan]AskIT-CLI[/bold cyan] - Your intelligent command-line assistant")
    console.print("\n[bold]Usage:[/bold]")
    console.print("  askit-cli [OPTIONS] -p <prompt>      # Ask a question (default)")
    console.print("  askit-cli [COMMAND]                  # Run specific command")
    
    console.print("\n[bold]Main Options:[/bold]")
    console.print("  [cyan]-p, --prompt[/cyan] TEXT     The user prompt to ask the AI [required for asking]")
    console.print("  [cyan]-c, --context[/cyan] INTEGER Number of shell history lines to send [default: 10]")
    console.print("  [cyan]--safe[/cyan]               Activates 'Safe Mode'")
    
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [cyan]init[/cyan]    Initialize AskIT project in current directory")
    console.print("  [cyan]config[/cyan]  Open interactive configuration shell")
    console.print("  [cyan]info[/cyan]    Show configuration paths and status")
    
    console.print("\n[bold]Global Options:[/bold]")
    console.print("  [cyan]--help[/cyan]               Show this help message and exit")
    console.print("  [cyan]--version[/cyan]            Show version and exit")
    
    console.print("\n[bold]Examples:[/bold]")
    console.print("  askit-cli -p 'create a backup script'")
    console.print("  askit-cli -c 20 --safe -p 'list all docker containers'")
    console.print("  askit-cli init")
    console.print("  askit-cli config                      # Auto-installs tab completion")
    console.print("  askit-cli info                        # Show config paths and status")
    
    console.print("\n[dim]For more information, visit: https://github.com/your-username/askit-cli[/dim]")


def ask_ai(prompt: str, context_lines: int = 10, safe_mode: bool = False):
    """
    Core ask functionality extracted as a separate function.
    Can now loop to ask for more information if needed.
    """
    console = Console()
    
    # Import heavy dependencies only when needed
    from dotenv import load_dotenv
    from .providers.claude import ClaudeProvider
    from .core.config_manager import ensure_config_directories, migrate_old_config_if_needed, get_config_file
    from .core.history import get_shell_history, format_history_context
    import yaml

    # Load environment variables only when needed
    load_dotenv()
    
    ensure_config_directories()
    migrate_old_config_if_needed()

    api_key = secrets_manager.get_api_key()
    if not api_key:
        console.print("[bold red]Error:[/bold red] API key not found. Run `askit-cli config` to set it.")
        raise typer.Exit(1)

    # Load configuration to check execution mode
    config_file = get_config_file()
    config = {"mode": "normal"}  # Default mode
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {"mode": "normal"}
        except Exception:
            pass
    execution_mode = config.get("mode", "normal")

    # --- Start of the interaction loop ---
    current_prompt = prompt
    
    while True:
        console.print(f"[dim]Analyzing request with {context_lines} lines of context...[/dim]")

        # Get shell history
        history_lines = get_shell_history(context_lines)
        formatted_history = format_history_context(history_lines)

        # Build context with OS information
        os_info = f"Operating System: {platform.system()} {platform.release()}"
        project_root = project.find_project_root()
        
        context_parts = [os_info]
        if project_root:
            context_parts.append(f"Project detected at: {project_root}")
        
        context_parts.append(f"Shell history (last {context_lines} lines):\n{formatted_history}")
        
        context = "\\n\\n".join(context_parts)
        
        # Show a nice progress indicator
        with console.status("[bold green]Asking Claude...", spinner="dots"):
            provider = ClaudeProvider(api_key=api_key)
            confidence, command, explanation = provider.get_suggestion(prompt=current_prompt, context=context)

        # --- Handle 'NONE' confidence: ask for more info and loop ---
        if confidence == "NONE":
            console.print("\n" + "="*60)
            console.print("[bold yellow]❓ Claude needs more information:[/bold yellow]")
            if explanation:
                console.print(f"\n{explanation}")
            console.print("="*60)
            
            try:
                # Ask user for more details
                new_info = Prompt.ask(
                    "[cyan]Please provide more details (or press Ctrl+C to cancel)[/cyan]"
                )
                # Append the new info to the prompt for the next loop to maintain conversation context
                current_prompt += f"\n\nClarification previously requested: '{explanation}'.\nUser provided additional details: '{new_info}'"
                continue # Restart the loop with the new prompt
            
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]❌ Operation cancelled by user.[/yellow]")
                raise typer.Exit()
        
        # --- If confidence is not NONE, break the loop and show results ---
        break

    # Display final results
    console.print("\n" + "="*60)
    console.print(f"[bold cyan]💡 Suggestion for:[/bold cyan] [italic]{prompt}[/italic]")
    console.print("="*60)
    
    # Handle the 'AGENT' confidence case
    if confidence == "AGENT":
        console.print("[bold magenta]🤖 Agent Task Detected[/bold magenta]")
        if explanation:
            console.print(f"\n[bold]Proposed Plan:[/bold]\n{explanation}")
        console.print("\n" + "="*60)
        
        try:
            confirm = Prompt.ask(
                "[cyan]Do you want to run this agent task?[/cyan]",
                choices=["y", "n"],
                default="y"
            )
            if confirm.lower() == 'y':
                from .agent.runtime import run_agent  # Import only when needed
                asyncio.run(run_agent(prompt, explanation, provider))
            else:
                console.print("[dim]Agent task cancelled.[/dim]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]❌ Operation cancelled by user.[/yellow]")
        raise typer.Exit()

    # Handle the 'NONE' confidence case first - this part is now unreachable but kept for safety
    if confidence == "NONE":
        console.print("[bold yellow]❓ Claude needs more information:[/bold yellow]")
        if explanation:
            console.print(f"\n{explanation}")
        console.print("\n" + "="*60)
        console.print("[dim]Please rephrase your request with more details.[/dim]")
        raise typer.Exit()
        
    # Show confidence level
    confidence_color = {"HIGH": "green", "MEDIUM": "yellow", "LOW": "red"}
    console.print(f"[{confidence_color.get(confidence, 'white')}]Confidence: {confidence}[/{confidence_color.get(confidence, 'white')}]")
    
    # Handle different modes
    if execution_mode == "strike" and confidence == "HIGH" and not safe_mode and command:
        # Strike mode with high confidence: pre-fill command
        console.print(f"\n[bold green]Ready to execute:[/bold green] [cyan]{command}[/cyan]")
        console.print(f"\n[dim]{explanation}[/dim]")
        console.print("\n" + "="*60)
        console.print("[bold yellow]Press Enter to execute, or Ctrl+C to cancel[/bold yellow]")
        
        try:
            input()  # Wait for user confirmation
            import subprocess
            import sys
            
            # On Windows, we must explicitly use PowerShell
            if sys.platform == "win32":
                # Using powershell.exe -Command ensures we run in the correct shell
                # and handle encoding properly for output.
                executable = ["powershell.exe", "-Command", command]
                shell_mode = False # We specify the executable, so shell=False
            else:
                # On other systems, the default shell is usually fine
                executable = command
                shell_mode = True

            result = subprocess.run(
                executable,
                shell=shell_mode,
                capture_output=True,
                text=True,
                errors='replace'
            )
                
            if result.returncode == 0:
                console.print(f"[green]✅ Command executed successfully[/green]")
                if result.stdout:
                    console.print(f"Output:\n{result.stdout}")
            else:
                console.print(f"[red]❌ Command failed with exit code {result.returncode}[/red]")
                if result.stderr:
                    console.print(f"Error:\n{result.stderr}")
        except KeyboardInterrupt:
            console.print("\n[yellow]❌ Execution cancelled by user[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Error executing command: {e}[/red]")
    else:
        # Normal mode or low confidence: just show suggestion
        if command:
            console.print(f"\n[bold]Command:[/bold] [cyan]{command}[/cyan]")
        if explanation:
            console.print(f"\n{explanation}")
        console.print("\n" + "="*60)
        
        if execution_mode == "strike" and confidence != "HIGH":
            console.print("[dim yellow]💡 Strike mode requires HIGH confidence for auto-execution[/dim yellow]")
        elif execution_mode == "strike" and safe_mode:
            console.print("[dim yellow]🛡️ Safe mode prevents auto-execution[/dim yellow]")
        elif execution_mode == "normal":
            console.print("[dim]ℹ️  Normal mode: Copy and execute commands manually[/dim]")


def parse_and_join_prompt(args: list[str]) -> tuple[list[str], str | None]:
    """
    Finds -p or --prompt, joins the subsequent words into a single string,
    and returns the remaining arguments along with the extracted prompt.
    """
    try:
        if "-p" in args:
            p_index = args.index("-p")
        elif "--prompt" in args:
            p_index = args.index("--prompt")
        else:
            return args, None  # No prompt flag found
    except ValueError:
        # Should not happen if one of the flags is present, but good practice
        return args, None

    # Get arguments before the flag
    remaining_args = args[:p_index]
    
    # Get words for the prompt
    prompt_words = []
    prompt_start_index = p_index + 1
    
    # Iterate from the word after the flag to the end of the arguments
    for i in range(prompt_start_index, len(args)):
        arg = args[i]
        # Stop if we hit another option
        if arg.startswith('-'):
            # This and subsequent args are not part of the prompt
            remaining_args.extend(args[i:])
            break
        prompt_words.append(arg)
    
    if not prompt_words:
        # This happens if -p is at the end of the command
        return remaining_args, None

    prompt = " ".join(prompt_words)
    return remaining_args, prompt


def main(args: Optional[list[str]] = None):
    """
    Main entry point for the CLI application.
    
    This function manually parses the prompt from sys.argv to allow for
    free-form prompts (e.g., `askit -p list all files`). If a prompt is
    found, it calls the core `ask_ai` function directly. Otherwise, it
    defers to Typer to handle other commands like `init`, `config`, etc.
    """
    # If no args are passed, use sys.argv. This makes it testable.
    if args is None:
        args = sys.argv[1:]

    remaining_args, prompt_text = parse_and_join_prompt(args)

    if prompt_text:
        # A prompt was found. We'll manually parse other known options.
        context_lines = 10
        safe_mode = False

        if "-c" in remaining_args:
            try:
                c_index = remaining_args.index("-c")
                context_lines = int(remaining_args[c_index + 1])
            except (ValueError, IndexError, TypeError):
                pass  # Ignore if malformed
        elif "--context" in remaining_args:
            try:
                c_index = remaining_args.index("--context")
                context_lines = int(remaining_args[c_index + 1])
            except (ValueError, IndexError, TypeError):
                pass
        
        if "--safe" in remaining_args:
            safe_mode = True
            
        ask_ai(prompt=prompt_text, context_lines=context_lines, safe_mode=safe_mode)
    else:
        # No prompt found. Let Typer handle other commands like `init`, `config`, `info`,
        # and global options like --help and --version.
        app(args)


app = typer.Typer(
    name="askit-cli",
    help="AskIT-CLI: Your intelligent command-line assistant.",
    add_completion=False,  # We handle completion manually
)
console = Console()


@app.command()
def init():
    """
    Initialize the AskIT project in the current directory.
    """
    init_project()


@app.command()
def config():
    """
    Open the interactive configuration shell.
    """
    # Vérifier et installer l'autocomplétion si nécessaire
    _check_and_install_completion()
    
    asyncio.run(config_shell())


@app.command()
def info():
    """
    Show information about askit-cli configuration paths and status.
    """
    from .core.config_manager import (
        get_config_dir, get_config_file, get_cache_dir, 
        get_data_dir, get_logs_dir
    )
    
    console.print("\n[bold cyan]AskIT-CLI Configuration Info[/bold cyan]")
    console.print(f"[dim]OS: {platform.system()} {platform.release()}[/dim]")
    
    console.print("\n[bold]Configuration Paths:[/bold]")
    console.print(f"  Config Dir:  [cyan]{get_config_dir()}[/cyan]")
    console.print(f"  Config File: [cyan]{get_config_file()}[/cyan]")
    console.print(f"  Cache Dir:   [cyan]{get_cache_dir()}[/cyan]")
    console.print(f"  Data Dir:    [cyan]{get_data_dir()}[/cyan]")
    console.print(f"  Logs Dir:    [cyan]{get_logs_dir()}[/cyan]")
    
    # Check if config file exists
    config_file = get_config_file()
    if config_file.exists():
        console.print(f"\n[bold green]✓[/bold green] Configuration file exists")
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
            console.print(f"  Mode: [green]{config.get('mode', 'normal')}[/green]")
        except Exception:
            console.print("  [yellow]Configuration file exists but couldn't be read[/yellow]")
    else:
        console.print(f"\n[yellow]⚠[/yellow] No configuration file found")
        console.print("  Run [cyan]askit-cli config[/cyan] to set up")
    
    # Check API key
    api_key = secrets_manager.get_api_key()
    if api_key:
        console.print(f"\n[bold green]✓[/bold green] API key is configured")
    else:
        console.print(f"\n[yellow]⚠[/yellow] No API key found")
        console.print("  Run [cyan]askit-cli config[/cyan] to set up")
    
    # Check if in a project
    project_root = project.find_project_root()
    if project_root:
        console.print(f"\n[bold green]✓[/bold green] AskIT project detected")
        console.print(f"  Project root: [cyan]{project_root}[/cyan]")
    else:
        console.print(f"\n[dim]ⓘ[/dim] Not in an AskIT project")
        console.print("  Run [cyan]askit-cli init[/cyan] to initialize a project")


def _detect_shell():
    """Détecte automatiquement le shell utilisé"""
    shell_env = os.environ.get('SHELL', '').lower()
    if 'bash' in shell_env:
        return 'bash'
    elif 'zsh' in shell_env:
        return 'zsh'
    elif 'fish' in shell_env:
        return 'fish'
    elif os.name == 'nt':  # Windows
        return 'powershell'
    return None


def _is_completion_installed():
    """Vérifie si l'autocomplétion est déjà installée"""
    from pathlib import Path
    
    shell = _detect_shell()
    if not shell:
        return True  # Si on ne peut pas détecter, on assume que c'est installé
    
    if shell == 'bash':
        completion_file = Path.home() / '.bash_completion.d' / 'askit-cli'
        return completion_file.exists()
    elif shell == 'zsh':
        completion_file = Path.home() / '.zsh' / 'completions' / '_askit-cli'
        return completion_file.exists()
    elif shell == 'fish':
        completion_file = Path.home() / '.config' / 'fish' / 'completions' / 'askit-cli.fish'
        return completion_file.exists()
    elif shell == 'powershell':
        # Pour PowerShell, on assume que c'est déjà géré
        return True
    
    return True


def _install_completion_for_shell(shell):
    """Installe l'autocomplétion pour le shell donné"""
    import subprocess
    from pathlib import Path
    
    try:
        if shell in ['bash', 'zsh', 'fish']:
            # Générer le script d'autocomplétion
            result = subprocess.run([
                sys.executable, "-c", 
                f"""
import typer
from typer.main import get_completion
completion = get_completion(prog_name='askit-cli', shell='{shell}')
print(completion)
"""
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                completion_script = result.stdout
                
                # Déterminer le chemin d'installation
                if shell == 'bash':
                    completion_dir = Path.home() / '.bash_completion.d'
                    completion_file = completion_dir / 'askit-cli'
                elif shell == 'zsh':
                    completion_dir = Path.home() / '.zsh' / 'completions'
                    completion_file = completion_dir / '_askit-cli'
                elif shell == 'fish':
                    completion_dir = Path.home() / '.config' / 'fish' / 'completions'
                    completion_file = completion_dir / 'askit-cli.fish'
                
                # Créer le dossier et installer
                completion_dir.mkdir(parents=True, exist_ok=True)
                completion_file.write_text(completion_script)
                
                console.print(f"[dim]✓ Autocomplétion installée pour {shell}[/dim]")
                return True
    
    except Exception:
        pass  # Installation silencieuse, on n'affiche pas les erreurs
    
    return False


def _check_and_install_completion():
    """Vérifie et installe l'autocomplétion si nécessaire"""
    if not _is_completion_installed():
        shell = _detect_shell()
        if shell:
            console.print("[dim]🔧 Installation de l'autocomplétion...[/dim]")
            _install_completion_for_shell(shell)


def version_callback(value: bool):
    """
    Callback to show version and exit.
    """
    if value:
        console = Console()
        console.print(f"askit-cli version: [bold green]{__version__}[/bold green]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def cli_main(
    ctx: typer.Context,
    prompt: Annotated[
        Optional[str],
        typer.Option("--prompt", "-p", help="The user prompt to ask the AI. All subsequent text is captured."),
    ] = None,
    context_lines: Annotated[
        int,
        typer.Option("--context", "-c", help="Number of shell history lines to send as context."),
    ] = 10,
    safe_mode: Annotated[
        bool,
        typer.Option("--safe", help="Activates 'Safe Mode', preventing automatic command execution."),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show version and exit.")
    ] = None,
):
    """
    AskIT: Your intelligent command-line assistant.
    """
    # The main "ask" logic is now handled in the `main` function.
    # This callback now primarily handles cases where a subcommand is invoked
    # or when no valid prompt is given, in which case we show help.
    if ctx.invoked_subcommand is None and prompt is None:
        # This condition is met when the user runs `askit-cli` with no args,
        # or with options that our manual parser didn't handle (like just `-c 10`).
        show_help()


if __name__ == "__main__":
    main(sys.argv[1:]) 