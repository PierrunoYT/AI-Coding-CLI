import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

# --- Configuration ---
class Config:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.app_url = os.getenv("APP_URL", "https://github.com/your-username/aichat-py")
        self.app_name = os.getenv("APP_NAME", "AI Chat CLI (Python)")
        self.default_model = "openai/gpt-4o"
        self.model = self.default_model

    def get_model(self):
        return self.model

    def set_model(self, model_id):
        self.model = model_id

# --- API Client ---
class ChatClient:
    def __init__(self, config):
        self.config = config
        self.api_base = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.config.app_url,
            "X-Title": self.config.app_name,
        }
        self.conversation_history = []
        self.total_tokens = 0
        self.total_cost = 0.0

    def get_available_models(self):
        try:
            response = requests.get(f"{self.api_base}/models")
            response.raise_for_status()
            models_data = response.json().get("data", [])
            return sorted(models_data, key=lambda x: x.get('id'))
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching models: {e}[/bold red]")
            return None

    def send_chat_request(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        
        payload = {
            "model": self.config.get_model(),
            "messages": self.conversation_history,
            "stream": True,
        }

        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True
            )
            response.raise_for_status()
            
            full_response = ""
            console.print("[bold cyan]AI:[/bold cyan] ", end="")
            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode('utf-8')
                    if chunk_str.startswith("data:"):
                        data_str = chunk_str[len("data: "):]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            
                            # Handle usage stats in the last message
                            if "usage" in data:
                                self.total_tokens += data['usage']['total_tokens']
                                # cost calculation might need pricing info
                                continue

                            delta = data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                full_response += content
                                console.print(content, end="")
                        except json.JSONDecodeError:
                            console.print(f"[bold red]Error decoding JSON stream chunk: {data_str}[/bold red]")
            
            console.print() # for newline
            self.conversation_history.append({"role": "assistant", "content": full_response})

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]API Error: {e}[/bold red]")
            self.conversation_history.pop() # remove user message if request failed

    def reset_conversation(self):
        self.conversation_history = []
        self.total_tokens = 0
        self.total_cost = 0.0
        console.print("[bold yellow]Conversation history reset.[/bold yellow]")

    def show_stats(self):
        table = Table(title="Conversation Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Model", self.config.get_model())
        table.add_row("Total Tokens", str(self.total_tokens))
        # table.add_row("Estimated Cost", f"${self.total_cost:.6f}") # Add cost calculation later
        table.add_row("History Length", f"{len(self.conversation_history)} messages")
        console.print(table)


# --- UI Functions ---
console = Console()

def print_help():
    markdown = Markdown("""
# AI Chat CLI Commands
- `/help`: Show this help message.
- `/model`: Show the current AI model.
- `/models`: List and select from available models.
- `/stats`: Show conversation statistics.
- `/reset`: Reset the conversation history.
- `/clear`: Clear the console screen.
- `/exit`: Exit the application.
    """)
    console.print(markdown)

def print_model_list(models):
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


# --- Main Application ---
def main():
    cfg = Config()
    if not cfg.api_key:
        console.print("[bold red]Error: OPENROUTER_API_KEY environment variable not set.[/bold red]")
        return
        
    client = ChatClient(cfg)

    console.print("[bold]Welcome to AI Chat CLI![/bold]")
    console.print(f"Type a message to start chatting or `/help` for commands.")
    console.print(f"Using model: [cyan]{client.config.get_model()}[/cyan]")

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