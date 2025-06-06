from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()

def print_help():
    """Display the help message with available commands."""
    markdown = Markdown("""
# AI Chat CLI Commands
- `/help`: Show this help message.
- `/model`: Show the current AI model.
- `/models`: List and select from available models.
- `/agent`: Toggle coding agent mode (enables file system tools).
- `/parallel`: Toggle tool execution mode (parallel/sequential).
- `/max-tools <number>`: Set maximum tool calls per response (1-20).
- `/stats`: Show conversation statistics.
- `/reset`: Reset the conversation history.
- `/clear`: Clear the console screen.
- `/exit`: Exit the application.

## Coding Agent Mode
When agent mode is enabled, the AI has access to these tools:
- **File Operations**: List, read, write, and delete files
- **Directory Operations**: Create directories and navigate file system
- **Code Execution**: Run Python scripts (with user confirmation)
- **Promise Detection**: Automatically detects when AI promises to use tools but doesn't

## Tool Execution Modes
- **Sequential**: Tools run one after another (safer, shows progress)
- **Parallel**: Tools run simultaneously (faster for independent operations)

## Smart Tool Promise Detection 🎯
The CLI now automatically detects when the AI says it will use a tool (like "let me check the files") but doesn't actually call the function. When this happens, you'll get a warning and option to make the AI follow through!

Agent mode is perfect for coding tasks, file management, and automation!
    """)
    console.print(markdown)

def print_model_list(models):
    """Display available models in a formatted table."""
    table = Table(title="Available OpenRouter Models")
    table.add_column("#", style="cyan")
    table.add_column("Model ID", style="green")
    table.add_column("Context (Tokens)", style="magenta")
    table.add_column("Price/M Tok (In/Out)", style="yellow")

    for i, model in enumerate(models):
        pricing = model.get('pricing', {})
        price_str = f"${float(pricing.get('prompt', 0)):.4f} / ${float(pricing.get('completion', 0)):.4f}"
        table.add_row(
            str(i + 1),
            model.get('id'),
            str(model.get('context_length')),
            price_str
        )
    console.print(table)

def select_model(chat_client):
    """Handle model selection UI interaction."""
    console.print("Fetching available models...")
    models = chat_client.get_available_models()
    if not models:
        return

    print_model_list(models)
    
    try:
        selection = console.input("[bold]Enter model number or type model handle (e.g., 'openai/gpt-4o'): [/bold]")
        
        if not selection:
            console.print("[yellow]No selection made. Keeping current model.[/yellow]")
            return

        # Try to parse as a number
        try:
            model_index = int(selection) - 1
            if 0 <= model_index < len(models):
                selected_model_id = models[model_index]['id']
                chat_client.config.set_model(selected_model_id)
                console.print(f"[bold green]✓ Model set to: {selected_model_id}[/bold green]")
                return
        except ValueError:
            # Not a number, treat as handle
            pass
        
        # Treat as a handle
        model_ids = [m['id'] for m in models]
        if selection in model_ids:
            chat_client.config.set_model(selection)
            console.print(f"[bold green]✓ Model set to: {selection}[/bold green]")
        else:
            console.print(f"[bold red]Invalid model handle: {selection}[/bold red]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Model selection cancelled.[/yellow]")

def display_welcome_message(client):
    """Display the welcome message and current configuration."""
    console.print("[bold green]✅ API connection successful![/bold green]")
    console.print("[bold]Welcome to AI Chat CLI![/bold]")
    console.print(f"Type a message to start chatting or `/help` for commands.")
    console.print(f"Using model: [cyan]{client.config.get_model()}[/cyan]")
    console.print(f"Agent mode: [yellow]{'🤖 ON' if client.config.agent_mode else '💬 OFF'}[/yellow] (type `/agent` to toggle)")
    if client.config.agent_mode:
        execution_emoji = "⚡" if client.config.tool_execution_mode == "parallel" else "🔄"
        console.print(f"Tool execution: [cyan]{execution_emoji} {client.config.tool_execution_mode.upper()}[/cyan] | Max tools: [cyan]{client.config.max_tool_calls}[/cyan]")

def handle_agent_toggle(client):
    """Handle agent mode toggle and display appropriate messages."""
    agent_status = client.config.toggle_agent_mode()
    status_text = "🤖 ON" if agent_status else "💬 OFF"
    console.print(f"[bold yellow]Agent mode: {status_text}[/bold yellow]")
    if agent_status:
        console.print("[green]✅ Coding agent tools are now available![/green]")
        execution_emoji = "⚡" if client.config.tool_execution_mode == "parallel" else "🔄"
        console.print(f"Tool execution: [cyan]{execution_emoji} {client.config.tool_execution_mode.upper()}[/cyan] | Max tools: [cyan]{client.config.max_tool_calls}[/cyan]")
    else:
        console.print("[yellow]💬 Back to regular chat mode.[/yellow]")

def handle_parallel_toggle(client):
    """Handle tool execution mode toggle."""
    if not client.config.agent_mode:
        console.print("[yellow]⚠️  Agent mode must be enabled to change tool execution mode.[/yellow]")
    else:
        execution_mode = client.config.toggle_tool_execution_mode()
        execution_emoji = "⚡" if execution_mode == "parallel" else "🔄"
        console.print(f"[bold cyan]Tool execution mode: {execution_emoji} {execution_mode.upper()}[/bold cyan]")
        if execution_mode == "parallel":
            console.print("[green]⚡ Tools will now run in parallel for faster execution![/green]")
        else:
            console.print("[yellow]🔄 Tools will now run sequentially for safer execution.[/yellow]")

def handle_max_tools_command(client, command):
    """Handle max tools configuration command."""
    if not client.config.agent_mode:
        console.print("[yellow]⚠️  Agent mode must be enabled to change max tool calls.[/yellow]")
    else:
        try:
            parts = command.split()
            if len(parts) == 2:
                max_tools = int(parts[1])
                if client.config.set_max_tool_calls(max_tools):
                    console.print(f"[bold green]✅ Maximum tool calls set to: {max_tools}[/bold green]")
                else:
                    console.print("[bold red]❌ Invalid number. Please use a number between 1 and 20.[/bold red]")
            else:
                console.print(f"[yellow]Current max tool calls: {client.config.max_tool_calls}[/yellow]")
                console.print("[yellow]Usage: /max-tools <number>[/yellow]")
        except ValueError:
            console.print("[bold red]❌ Please provide a valid number.[/bold red]")