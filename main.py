from rich.console import Console
from config import Config
from chat_client import ChatClient
from ui import (print_help, select_model, display_welcome_message, 
                handle_agent_toggle, handle_parallel_toggle, handle_max_tools_command)

console = Console()


def main():
    """Main application entry point."""
    cfg = Config()
    if not cfg.api_key:
        console.print("[bold red]Error: OPENROUTER_API_KEY environment variable not set.[/bold red]")
        console.print("[yellow]Please set your OpenRouter API key: export OPENROUTER_API_KEY=your_key_here[/yellow]")
        return
    
    try:    
        client = ChatClient(cfg)
    except ValueError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return

    # Test API connection
    console.print("[cyan]Testing API connection...[/cyan]")
    if not client.test_api_connection():
        console.print("[bold red]Failed to connect to OpenRouter API. Please check your API key and internet connection.[/bold red]")
        return

    display_welcome_message(client)

    try:
        while True:
            user_input = console.input("[bold green]You:[/bold green] ")

            if user_input.startswith('/'):
                command = user_input.lower().strip()
                if command == "/exit":
                    break
                elif command == "/help":
                    print_help()
                elif command == "/reset":
                    client.reset_conversation()
                elif command == "/clear":
                    console.clear()
                elif command == "/model":
                    console.print(f"Current model: [cyan]{client.config.get_model()}[/cyan]")
                elif command == "/models":
                    select_model(client)
                elif command == "/agent":
                    handle_agent_toggle(client)
                elif command == "/parallel":
                    handle_parallel_toggle(client)
                elif command.startswith("/max-tools"):
                    handle_max_tools_command(client, command)
                elif command == "/stats":
                    client.show_stats()
                else:
                    console.print(f"[yellow]Unknown command: {command}. Type /help for options.[/yellow]")
            else:
                client.send_chat_request(user_input)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold yellow]Exiting application. Goodbye![/bold yellow]")

if __name__ == "__main__":
    main() 