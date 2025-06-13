from pathlib import Path
import typer
from rich.console import Console

console = Console()

def init_project():
    """
    Project initialization logic. Creates the .askit directory.
    """
    project_path = Path.cwd()
    askit_dir = project_path / ".askit"

    if askit_dir.is_dir():
        console.print(f"The [bold green]AskIT[/bold green] project has already been initialized in [cyan]{project_path}[/cyan].")
        raise typer.Exit()

    try:
        askit_dir.mkdir()
        (askit_dir / "logs").mkdir()
        
        config_path = askit_dir / "config.yaml"
        config_path.touch() # Create an empty file to start

        console.print(f"🚀 [bold green]AskIT[/bold green] project initialized successfully in [cyan]{askit_dir}[/cyan].")
        console.print("You can now run `askit-cli config` to set up your API key.")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Could not initialize the project. {e}")
        raise typer.Exit(code=1) 