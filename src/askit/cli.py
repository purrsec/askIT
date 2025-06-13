import typer
from rich.console import Console
import asyncio
from typing_extensions import Annotated
import sys
import os
from typing import Optional

from .commands.init_cmd import init_project
from .commands.config_cmd import config_shell
from .core import project
from .security import secrets_manager
from .providers.claude import ClaudeProvider
from dotenv import load_dotenv

load_dotenv()

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
    
    console.print("\n[bold]Global Options:[/bold]")
    console.print("  [cyan]--help[/cyan]               Show this help message and exit")
    console.print("  [cyan]--version[/cyan]            Show version and exit")
    
    console.print("\n[bold]Examples:[/bold]")
    console.print("  askit-cli -p 'create a backup script'")
    console.print("  askit-cli -c 20 --safe -p 'list all docker containers'")
    console.print("  askit-cli init")
    console.print("  askit-cli config")
    
    console.print("\n[dim]For more information, visit: https://github.com/your-username/askit-cli[/dim]")


def ask_ai(prompt: str, context_lines: int = 10, safe_mode: bool = False):
    """
    Core ask functionality extracted as a separate function.
    """
    console = Console()
    console.print("[bold cyan]Running main logic...[/bold cyan]")

    if not project.find_project_root():
        console.print("[bold red]Error:[/bold red] Not in an AskIT project. Run `askit-cli init` first.")
        raise typer.Exit(1)

    api_key = secrets_manager.get_api_key()
    if not api_key:
        console.print("[bold red]Error:[/bold red] API key not found. Run `askit-cli config` to set it.")
        raise typer.Exit(1)

    # This is a placeholder for context building.
    context = f"Shell history (last {context_lines} lines):\n... (not implemented yet) ..."

    # Provider selection will be made configurable later.
    provider = ClaudeProvider(api_key=api_key)
    suggestion = provider.get_suggestion(prompt=prompt, context=context)

    console.print("\n[bold green]Suggestion:[/bold green]")
    console.print(suggestion)


def main():
    """
    Main entry point that handles the no-arguments case gracefully.
    """
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        show_help()
        return
    
    # If only whitespace arguments, show help
    if len(sys.argv) > 1 and all(arg.strip() == "" for arg in sys.argv[1:]):
        show_help()
        return
    
    # Otherwise, let Typer handle normally
    app()


app = typer.Typer(
    name="askit-cli",
    help="AskIT-CLI: Your intelligent command-line assistant.",
    add_completion=False,
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
    asyncio.run(config_shell())


@app.callback(invoke_without_command=True)
def cli_main(
    ctx: typer.Context,
    prompt: Annotated[
        Optional[str],
        typer.Option("--prompt", "-p", help="The user prompt to ask the AI."),
    ] = None,
    context_lines: Annotated[
        int,
        typer.Option("--context", "-c", help="Number of shell history lines to send as context."),
    ] = 10,
    safe_mode: Annotated[
        bool,
        typer.Option("--safe", help="Activates 'Safe Mode'.")
    ] = False,
):
    """
    AskIT-CLI: Your intelligent command-line assistant.
    
    By default, asks a question to the AI. Use specific commands for other actions.
    """
    # If a subcommand is being invoked, let it handle itself
    if ctx.invoked_subcommand is not None:
        return
    
    # If no prompt provided, this is an error since we're in the main flow
    if prompt is None:
        console.print("[bold red]Error:[/bold red] Prompt is required. Use -p or --prompt to specify your question.")
        console.print("\nTry: [cyan]askit-cli -p 'your question here'[/cyan]")
        console.print("Or:  [cyan]askit-cli --help[/cyan] for more information")
        raise typer.Exit(1)
    
    # Call the ask functionality
    ask_ai(prompt, context_lines, safe_mode)


if __name__ == "__main__":
    main() 