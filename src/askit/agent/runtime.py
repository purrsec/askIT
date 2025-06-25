import re
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
import shutil
import sys
from ..providers.base_provider import AIBaseProvider

console = Console()

def execute_shell_command(command: str):
    """Executes a shell command and prints its output."""
    try:
        console.print(f"[bold cyan]▶ Executing:[/bold cyan] [dim]{command}[/dim]")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, encoding='utf-8', errors='replace'
        )
        for line in iter(process.stdout.readline, ''):
            console.print(f"[dim]  {line.strip()}[/dim]")
        process.stdout.close()
        return_code = process.wait()
        if return_code:
            console.print(f"[bold red]✗ Command failed with exit code {return_code}[/bold red]")
            return False
        else:
            console.print(f"[bold green]✓ Command finished successfully[/bold green]")
            return True
    except Exception as e:
        console.print(f"[bold red]✗ Failed to execute command:[/bold red] {e}")
        return False

def create_file(file_path: str, content: str):
    """Creates a file with the given content, creating parent directories if needed."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        console.print(f"[bold green]✓ Created file:[/bold green] [yellow]{file_path}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to create file {file_path}:[/bold red] {e}")

def check_tool_is_installed(tool_name: str) -> bool:
    """Checks if a command-line tool is installed and in the system's PATH."""
    return shutil.which(tool_name) is not None

async def get_installation_command(tool_name: str, provider: AIBaseProvider) -> str:
    """Asks the AI for the command to install a missing tool."""
    os_name = sys.platform
    if os_name == 'darwin':
        os_name = 'macOS'
    elif os_name.startswith('linux'):
        os_name = 'Linux'
    elif os_name == 'win32':
        os_name = 'Windows'
    
    prompt = f"The command-line tool '{tool_name}' is not found on my {os_name} system. Provide the most common, single-line command to install it. Only the command, no other text."
    confidence, command, _ = provider.get_suggestion(prompt=prompt, context="Provide an installation command.")
    
    return command if confidence in ["HIGH", "MEDIUM"] and command else ""

async def run_agent(initial_prompt: str, explanation: str, provider: AIBaseProvider):
    """
    Runs the autonomous agent mode by parsing and executing a plan.
    Includes a pre-flight check for required tools.
    """
    console.print(f"[bold magenta]🚀 Agent Mode Activated[/bold magenta]")
    console.print(f"[dim]Initial objective:[/dim] [italic]{initial_prompt}[/italic]")
    console.print()

    bash_command_pattern = re.compile(r"```bash\n(.*?)\n```", re.DOTALL)
    file_creation_pattern = re.compile(r"FILE: ([\w\./\\\{\}-]+)\n```(?:\w+)?\n(.*?)\n```", re.DOTALL)
    user_input_pattern = re.compile(r"\{\{USER_INPUT:(.*?)\}\}")

    # --- Collect User Input ---
    console.print("[bold]📝 The agent needs more information to proceed...[/bold]")
    user_inputs = {}
    placeholders = user_input_pattern.findall(explanation)
    
    # Use a set to only ask for each unique placeholder once
    unique_placeholders = sorted(list(set(placeholders)), key=placeholders.index)

    if not unique_placeholders:
        console.print("[dim]  - No user input required.[/dim]")
    else:
        for placeholder in unique_placeholders:
            # Use Rich's Prompt for a better user experience
            user_response = Prompt.ask(f"[bold yellow]❓ {placeholder}[/bold yellow]")
            user_inputs[f"{{{{USER_INPUT:{placeholder}}}}}"] = user_response

        # Replace placeholders in the explanation
        for placeholder, value in user_inputs.items():
            explanation = explanation.replace(placeholder, value)
            
    console.print("[bold green]✅ Information collected.[/bold green]\n")

    # --- Pre-flight Checks ---
    console.print("[bold]🕵️  Performing pre-flight checks...[/bold]")
    required_tools = set()
    all_commands = [cmd.strip() for match in bash_command_pattern.finditer(explanation) for cmd in match.group(1).strip().split('\n') if cmd.strip()]

    for command in all_commands:
        tool_name = command.split(' ')[0]
        if tool_name not in ['mkdir', 'cd', 'echo', 'ls', 'cat', 'rm', 'mv', 'cp']:
            required_tools.add(tool_name)

    if not required_tools:
        console.print("[dim]  - No external tools required.[/dim]")
    else:
        console.print(f"[dim]  - Required tools: {', '.join(required_tools)}[/dim]")
        for tool in sorted(list(required_tools)):
            if not check_tool_is_installed(tool):
                console.print(f"[bold yellow]⚠️ Tool not found:[/bold yellow] [cyan]{tool}[/cyan]")
                install_command = await get_installation_command(tool, provider)
                if install_command:
                    console.print(f"[dim]  - AI suggests this command for installation:[/dim] [green]{install_command}[/green]")
                    if Confirm.ask(f"Do you want to run this command to install '{tool}'?", default=True):
                        execute_shell_command(install_command)
                        if not check_tool_is_installed(tool):
                            console.print(f"[bold red]✗ Agent stopped: Could not install '{tool}'. Please install it manually and try again.[/bold red]")
                            return
                        console.print(f"[bold green]✓ Tool '{tool}' is now ready.[/bold green]")
                    else:
                        console.print(f"[bold red]✗ Agent stopped: Required tool '{tool}' not installed.[/bold red]")
                        return
                else:
                    console.print(f"[bold red]✗ Agent stopped: Could not find installation instructions for '{tool}'. Please install it manually.[/bold red]")
                    return
    
    console.print("[bold green]✅ Pre-flight checks passed.[/bold green]\n")

    # --- Plan Execution ---
    console.print("[bold]Executing plan...[/bold]")
    for command in all_commands:
        if not execute_shell_command(command):
            console.print("[bold red]✗ Agent stopped due to a command failure.[/bold red]")
            return

    all_files = [(match.group(1).strip(), match.group(2).strip()) for match in file_creation_pattern.finditer(explanation)]

    for file_path, content in all_files:
        create_file(file_path, content)
    
    console.print("\n[bold green]✅ Agent has finished executing the plan.[/bold green]")
