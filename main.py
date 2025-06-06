import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from tools import TOOLS_DEFINITIONS, AVAILABLE_TOOLS

# --- Configuration ---
class Config:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.app_url = os.getenv("APP_URL", "https://github.com/your-username/aichat-py")
        self.app_name = os.getenv("APP_NAME", "AI Chat CLI (Python)")
        self.default_model = "openai/gpt-4o"
        self.model = self.default_model
        self.agent_mode = False  # Toggle for coding agent mode

    def get_model(self):
        return self.model

    def set_model(self, model_id):
        self.model = model_id
    
    def toggle_agent_mode(self):
        self.agent_mode = not self.agent_mode
        return self.agent_mode

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
        
        # Add system message for agent mode if not already present
        if self.config.agent_mode and (not self.conversation_history or 
                                     self.conversation_history[0].get("role") != "system"):
            system_message = {
                "role": "system", 
                "content": "You are a helpful coding assistant with access to file system tools. You can list files, read files, write files, execute Python scripts, create directories, and delete files. Use these tools when the user asks you to work with files or code. Always explain what you're doing before using tools."
            }
            self.conversation_history.insert(0, system_message)
        
        payload = {
            "model": self.config.get_model(),
            "messages": self.conversation_history,
            "stream": False,  # Disable streaming for function calls
        }
        
        # Add tools if in agent mode
        if self.config.agent_mode:
            payload["tools"] = TOOLS_DEFINITIONS
            payload["tool_choice"] = "auto"

        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            # Handle usage stats
            if "usage" in data:
                self.total_tokens += data['usage']['total_tokens']
            
            ai_message = data['choices'][0]['message']
            self.conversation_history.append(ai_message)
            
            # Check if AI wants to use tools
            if ai_message.get('tool_calls'):
                console.print("[bold cyan]🤖 Assistant is using tools...[/bold cyan]")
                
                for tool_call in ai_message['tool_calls']:
                    function_name = tool_call['function']['name']
                    function_to_call = AVAILABLE_TOOLS.get(function_name)
                    
                    if function_to_call:
                        function_args = json.loads(tool_call['function']['arguments'])
                        console.print(f"   🔧 Calling `{function_name}` with args: {function_args}")
                        
                        # Call the actual Python function
                        function_response = function_to_call(**function_args)
                        console.print(f"   📋 Tool response: {function_response}")
                        
                        # Add tool response to conversation
                        self.conversation_history.append({
                            "tool_call_id": tool_call['id'],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                
                # Get final response after tool execution
                final_payload = {
                    "model": self.config.get_model(),
                    "messages": self.conversation_history,
                    "tools": TOOLS_DEFINITIONS,
                    "tool_choice": "auto"
                }
                
                final_response = requests.post(
                    f"{self.api_base}/chat/completions",
                    headers=self.headers,
                    json=final_payload
                )
                final_response.raise_for_status()
                final_data = final_response.json()
                
                if "usage" in final_data:
                    self.total_tokens += final_data['usage']['total_tokens']
                
                final_message = final_data['choices'][0]['message']
                console.print(f"\n[bold cyan]AI:[/bold cyan] {final_message['content']}")
                self.conversation_history.append(final_message)
            else:
                # No tools called, just print the response
                console.print(f"[bold cyan]AI:[/bold cyan] {ai_message['content']}")

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
- `/agent`: Toggle coding agent mode (enables file system tools).
- `/stats`: Show conversation statistics.
- `/reset`: Reset the conversation history.
- `/clear`: Clear the console screen.
- `/exit`: Exit the application.

## Coding Agent Mode
When agent mode is enabled, the AI has access to these tools:
- **File Operations**: List, read, write, and delete files
- **Directory Operations**: Create directories and navigate file system
- **Code Execution**: Run Python scripts (with user confirmation)

Agent mode is perfect for coding tasks, file management, and automation!
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
    console.print(f"Agent mode: [yellow]{'🤖 ON' if client.config.agent_mode else '💬 OFF'}[/yellow] (type `/agent` to toggle)")

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
                    agent_status = client.config.toggle_agent_mode()
                    status_text = "🤖 ON" if agent_status else "💬 OFF"
                    console.print(f"[bold yellow]Agent mode: {status_text}[/bold yellow]")
                    if agent_status:
                        console.print("[green]✅ Coding agent tools are now available![/green]")
                    else:
                        console.print("[yellow]💬 Back to regular chat mode.[/yellow]")
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