import os
import requests
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from tools import TOOLS_DEFINITIONS, AVAILABLE_TOOLS
import re

# --- Configuration ---
class Config:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.app_url = os.getenv("APP_URL", "https://github.com/your-username/aichat-py")
        self.app_name = os.getenv("APP_NAME", "AI Chat CLI (Python)")
        self.default_model = "openai/gpt-4o"
        self.model = self.default_model
        self.agent_mode = False  # Toggle for coding agent mode
        self.tool_execution_mode = "sequential"  # "sequential" or "parallel"
        self.max_tool_calls = 10  # Maximum tool calls per response
        self.debug = os.getenv("DEBUG", "false").lower() == "true"  # Debug mode

    def get_model(self):
        return self.model

    def set_model(self, model_id):
        self.model = model_id
    
    def toggle_agent_mode(self):
        self.agent_mode = not self.agent_mode
        return self.agent_mode
    
    def toggle_tool_execution_mode(self):
        if self.tool_execution_mode == "sequential":
            self.tool_execution_mode = "parallel"
        else:
            self.tool_execution_mode = "sequential"
        return self.tool_execution_mode
    
    def set_max_tool_calls(self, max_calls):
        if max_calls > 0 and max_calls <= 20:
            self.max_tool_calls = max_calls
            return True
        return False

# --- API Client ---
class ChatClient:
    def __init__(self, config):
        self.config = config
        self.api_base = "https://openrouter.ai/api/v1"
        
        # Validate API key
        if not self.config.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        if not self.config.api_key.startswith('sk-'):
            console.print(f"[yellow]⚠️  Warning: API key doesn't look like a typical OpenRouter key (should start with 'sk-')[/yellow]")
        
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.config.app_url,
            "X-Title": self.config.app_name,
        }
        self.conversation_history = []
        self.total_tokens = 0
        self.total_cost = 0.0

    def test_api_connection(self):
        """Test if the API key and connection work"""
        try:
            response = requests.get(f"{self.api_base}/models", headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                console.print("[bold red]❌ Authentication failed. Please check your OPENROUTER_API_KEY.[/bold red]")
            elif response.status_code == 403:
                console.print("[bold red]❌ Access forbidden. Your API key may not have the required permissions.[/bold red]")
            else:
                console.print(f"[bold red]❌ API test failed with HTTP {response.status_code}: {e}[/bold red]")
            return False
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]❌ Connection test failed: {e}[/bold red]")
            return False

    def get_available_models(self):
        try:
            response = requests.get(f"{self.api_base}/models", headers=self.headers)
            response.raise_for_status()
            models_data = response.json().get("data", [])
            return sorted(models_data, key=lambda x: x.get('id'))
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching models: {e}[/bold red]")
            return None

    def _detect_promised_but_uncalled_tools(self, ai_message_content):
        """
        Detect when AI promises to use tools but doesn't actually call them.
        Returns a list of tools that were promised but not called.
        """
        if not ai_message_content:
            return []
        
        # Common patterns where AI promises to use tools
        promise_patterns = [
            r"let me (?:check|list|read|write|create|delete|execute|run)\s+(?:the\s+)?(.+)",
            r"I(?:'ll|'m going to|will) (?:check|list|read|write|create|delete|execute|run)\s+(?:the\s+)?(.+)",
            r"(?:checking|listing|reading|writing|creating|deleting|executing|running)\s+(?:the\s+)?(.+)",
            r"I(?:'ll|will) (?:now\s+)?(?:proceed to\s+)?(?:check|list|read|write|create|delete|execute|run)",
        ]
        
        promised_actions = []
        content_lower = ai_message_content.lower()
        
        for pattern in promise_patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            promised_actions.extend(matches)
        
        # Look for specific tool-related keywords
        tool_keywords = [
            "file list", "directory", "check the file", "read the file", 
            "write to", "create file", "delete file", "list files"
        ]
        
        found_promises = []
        for keyword in tool_keywords:
            if keyword in content_lower:
                found_promises.append(keyword)
        
        return found_promises

    def send_chat_request(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        
        # Add system message for agent mode if not already present
        if self.config.agent_mode and (not self.conversation_history or 
                                     self.conversation_history[0].get("role") != "system"):
            system_message = {
                "role": "system", 
                "content": "You are a helpful coding assistant with access to file system tools. You can list files, read files, write files, execute Python scripts, create directories, and delete files. Use these tools when the user asks you to work with files or code. Always explain what you're doing before using tools. IMPORTANT: When you promise to use a tool (like 'let me check the files' or 'I'll read that file'), you MUST actually call the appropriate tool function. Don't just say you will do something - actually do it by calling the function."
            }
            self.conversation_history.insert(0, system_message)
        
        payload = {
            "model": self.config.get_model(),
            "messages": self.conversation_history,
            "stream": False,  # Disable streaming for function calls
        }
        
        # Add tools if in agent mode
        if self.config.agent_mode:
            # Check if the model supports function calling
            model_id = self.config.get_model().lower()
            supports_functions = any(x in model_id for x in ['gpt-4', 'gpt-3.5', 'claude', 'gemini'])
            
            if supports_functions:
                payload["tools"] = TOOLS_DEFINITIONS
                payload["tool_choice"] = "auto"
            else:
                console.print(f"[yellow]⚠️  Model '{self.config.get_model()}' may not support function calling. Consider using gpt-4o, claude-3, or another compatible model.[/yellow]")

        if self.config.debug:
            console.print(f"[dim]Debug: Sending request to {self.api_base}/chat/completions[/dim]")
            console.print(f"[dim]Debug: Model = {payload.get('model')}, Agent mode = {self.config.agent_mode}[/dim]")
            if 'tools' in payload:
                console.print(f"[dim]Debug: Including {len(payload['tools'])} tools[/dim]")

        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                # Try again without tool_choice if it's a 400 error in agent mode
                if self.config.agent_mode and "tool_choice" in payload:
                    console.print("[yellow]⚠️  Tool choice parameter causing issues, retrying without it...[/yellow]")
                    payload_retry = payload.copy()
                    del payload_retry["tool_choice"]
                    
                    response = requests.post(
                        f"{self.api_base}/chat/completions",
                        headers=self.headers,
                        json=payload_retry
                    )
                    response.raise_for_status()
                    data = response.json()
                else:
                    # Print detailed error info for debugging
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', str(e))
                        console.print(f"[bold red]API Error (400): {error_msg}[/bold red]")
                    except:
                        console.print(f"[bold red]API Error (400): {e}[/bold red]")
                    self.conversation_history.pop() # remove user message if request failed
                    return
            else:
                raise
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]API Error: {e}[/bold red]")
            self.conversation_history.pop() # remove user message if request failed
            return

        # Handle usage stats
        if "usage" in data:
            self.total_tokens += data['usage']['total_tokens']
        
        ai_message = data['choices'][0]['message']
        ai_content = ai_message.get('content', '')
        
        # Check if AI wants to use tools
        if ai_message.get('tool_calls'):
            tool_calls = ai_message['tool_calls']
            num_tools = len(tool_calls)
            
            # Limit the number of tool calls for safety
            if num_tools > self.config.max_tool_calls:
                console.print(f"[bold red]⚠️  Too many tool calls requested ({num_tools}). Limiting to {self.config.max_tool_calls}.[/bold red]")
                tool_calls = tool_calls[:self.config.max_tool_calls]
                num_tools = len(tool_calls)
            
            execution_mode = self.config.tool_execution_mode
            console.print(f"[bold cyan]🤖 Assistant is using {num_tools} tool(s) in {execution_mode} mode...[/bold cyan]")
            
            self.conversation_history.append(ai_message)
            
            if execution_mode == "parallel" and num_tools > 1:
                # Execute tools in parallel
                self._execute_tools_parallel(tool_calls)
            else:
                # Execute tools sequentially
                self._execute_tools_sequential(tool_calls)
                
            # Get final response after tool execution
            final_payload = {
                "model": self.config.get_model(),
                "messages": self.conversation_history,
                "stream": False,
            }
            
            # Only add tools if the model supports them
            model_id = self.config.get_model().lower()
            supports_functions = any(x in model_id for x in ['gpt-4', 'gpt-3.5', 'claude', 'gemini'])
            if supports_functions:
                final_payload["tools"] = TOOLS_DEFINITIONS
                final_payload["tool_choice"] = "auto"
            
            try:
                final_response = requests.post(
                    f"{self.api_base}/chat/completions",
                    headers=self.headers,
                    json=final_payload
                )
                final_response.raise_for_status()
                final_data = final_response.json()
            except requests.exceptions.HTTPError as e:
                if final_response.status_code == 400:
                    # Try again without tool_choice if it's a 400 error
                    console.print("[yellow]⚠️  Tool choice parameter causing issues in final call, retrying without it...[/yellow]")
                    final_payload_retry = final_payload.copy()
                    if "tool_choice" in final_payload_retry:
                        del final_payload_retry["tool_choice"]
                    
                    final_response = requests.post(
                        f"{self.api_base}/chat/completions",
                        headers=self.headers,
                        json=final_payload_retry
                    )
                    final_response.raise_for_status()
                    final_data = final_response.json()
                else:
                    console.print(f"[bold red]API Error in final call: {e}[/bold red]")
                    return
            except requests.exceptions.RequestException as e:
                console.print(f"[bold red]API Error in final call: {e}[/bold red]")
                return
            
            if "usage" in final_data:
                self.total_tokens += final_data['usage']['total_tokens']
            
            final_message = final_data['choices'][0]['message']
            final_content = final_message.get('content', '')
            
            # Check if AI wants to use more tools in the final response
            if final_message.get('tool_calls'):
                # Handle additional tool calls if needed (recursive case)
                console.print("[yellow]⚠️  AI wants to use more tools in response. This might indicate a complex workflow.[/yellow]")
                self.conversation_history.append(final_message)
                return self.send_chat_request("")  # Continue with empty message to process additional tools
            else:
                            # Display the final AI response
            self.conversation_history.append(final_message)
            if final_content:
                console.print("[bold blue]AI:[/bold blue]")
                markdown_content = Markdown(final_content)
                console.print(markdown_content)
            else:
                console.print("[bold blue]AI:[/bold blue] [italic]AI provided tool results but no additional commentary.[/italic]")
                
        else:
            # AI didn't call tools - check if it promised to use any
            if self.config.agent_mode and ai_content:
                promised_tools = self._detect_promised_but_uncalled_tools(ai_content)
                
                if promised_tools:
                    console.print(f"[bold yellow]⚠️  AI promised to use tools but didn't call them: {', '.join(promised_tools)}[/bold yellow]")
                    console.print("[yellow]This might be an AI oversight. The response was provided without tool execution.[/yellow]")
                    
                    # Ask user if they want to retry
                    retry = console.input("[bold]Would you like me to ask the AI to actually follow through? (y/N): [/bold]").lower().strip()
                    
                    if retry == 'y':
                        # Don't add the problematic AI message to history yet
                        # Add a follow-up message to encourage tool use
                        follow_up = "Please actually follow through with the tools you mentioned. Don't just describe what you would do - actually call the appropriate functions to perform the actions you promised."
                        console.print("[dim]Asking AI to follow through with promised actions...[/dim]")
                        return self.send_chat_request(follow_up)
            
                    # Add AI message to conversation and display it
        self.conversation_history.append(ai_message)
        if ai_content:
            console.print("[bold blue]AI:[/bold blue]")
            markdown_content = Markdown(ai_content)
            console.print(markdown_content)
        else:
            console.print("[bold blue]AI:[/bold blue] [italic]AI sent an empty response.[/italic]")

    def _execute_single_tool(self, tool_call):
        """Execute a single tool call and return the result."""
        function_name = tool_call['function']['name']
        function_to_call = AVAILABLE_TOOLS.get(function_name)
        
        if not function_to_call:
            return {
                "tool_call_id": tool_call['id'],
                "role": "tool",
                "name": function_name,
                "content": f"❌ Error: Tool '{function_name}' not found.",
            }
        
        try:
            function_args = json.loads(tool_call['function']['arguments'])
            start_time = time.time()
            function_response = function_to_call(**function_args)
            execution_time = time.time() - start_time
            
            return {
                "tool_call_id": tool_call['id'],
                "role": "tool", 
                "name": function_name,
                "content": function_response,
                "execution_time": execution_time,
                "args": function_args
            }
        except json.JSONDecodeError as e:
            return {
                "tool_call_id": tool_call['id'],
                "role": "tool",
                "name": function_name,
                "content": f"❌ Error parsing arguments: {e}",
            }
        except Exception as e:
            return {
                "tool_call_id": tool_call['id'],
                "role": "tool",
                "name": function_name,
                "content": f"❌ Error executing tool: {e}",
            }

    def _execute_tools_sequential(self, tool_calls):
        """Execute tools one after another in sequence."""
        for i, tool_call in enumerate(tool_calls, 1):
            function_name = tool_call['function']['name']
            console.print(f"   🔧 [{i}/{len(tool_calls)}] Calling `{function_name}`...")
            
            result = self._execute_single_tool(tool_call)
            
            # Display result
            if "execution_time" in result:
                console.print(f"   📋 Tool response ({result['execution_time']:.2f}s): {result['content']}")
            else:
                console.print(f"   📋 Tool response: {result['content']}")
            
            # Add to conversation history
            self.conversation_history.append({
                "tool_call_id": result["tool_call_id"],
                "role": result["role"],
                "name": result["name"],
                "content": result["content"],
            })

    def _execute_tools_parallel(self, tool_calls):
        """Execute tools in parallel using threading."""
        console.print("   ⚡ Executing tools in parallel...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=True
        ) as progress:
            
            task = progress.add_task("Running tools...", total=len(tool_calls))
            
            with ThreadPoolExecutor(max_workers=min(len(tool_calls), 5)) as executor:
                # Submit all tool calls
                future_to_tool = {
                    executor.submit(self._execute_single_tool, tool_call): tool_call 
                    for tool_call in tool_calls
                }
                
                completed_results = []
                
                # Collect results as they complete
                for future in as_completed(future_to_tool):
                    tool_call = future_to_tool[future]
                    result = future.result()
                    completed_results.append(result)
                    
                    function_name = tool_call['function']['name']
                    if "execution_time" in result:
                        console.print(f"   ✅ `{function_name}` completed ({result['execution_time']:.2f}s)")
                    else:
                        console.print(f"   ✅ `{function_name}` completed")
                    
                    progress.advance(task)
        
        # Sort results by original order and add to conversation
        tool_call_ids = [tc['id'] for tc in tool_calls]
        sorted_results = sorted(completed_results, key=lambda r: tool_call_ids.index(r['tool_call_id']))
        
        console.print("\n   📋 Tool Results:")
        for i, result in enumerate(sorted_results, 1):
            console.print(f"   {i}. {result['name']}: {result['content']}")
            
            # Add to conversation history
            self.conversation_history.append({
                "tool_call_id": result["tool_call_id"],
                "role": result["role"],
                "name": result["name"],
                "content": result["content"],
            })

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
        table.add_row("Agent Mode", "🤖 ON" if self.config.agent_mode else "💬 OFF")
        if self.config.agent_mode:
            execution_emoji = "⚡" if self.config.tool_execution_mode == "parallel" else "🔄"
            table.add_row("Tool Execution", f"{execution_emoji} {self.config.tool_execution_mode.upper()}")
            table.add_row("Max Tool Calls", str(self.config.max_tool_calls))
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

    console.print("[bold green]✅ API connection successful![/bold green]")
    console.print("[bold]Welcome to AI Chat CLI![/bold]")
    console.print(f"Type a message to start chatting or `/help` for commands.")
    console.print(f"Using model: [cyan]{client.config.get_model()}[/cyan]")
    console.print(f"Agent mode: [yellow]{'🤖 ON' if client.config.agent_mode else '💬 OFF'}[/yellow] (type `/agent` to toggle)")
    if client.config.agent_mode:
        execution_emoji = "⚡" if client.config.tool_execution_mode == "parallel" else "🔄"
        console.print(f"Tool execution: [cyan]{execution_emoji} {client.config.tool_execution_mode.upper()}[/cyan] | Max tools: [cyan]{client.config.max_tool_calls}[/cyan]")

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
                        execution_emoji = "⚡" if client.config.tool_execution_mode == "parallel" else "🔄"
                        console.print(f"Tool execution: [cyan]{execution_emoji} {client.config.tool_execution_mode.upper()}[/cyan] | Max tools: [cyan]{client.config.max_tool_calls}[/cyan]")
                    else:
                        console.print("[yellow]💬 Back to regular chat mode.[/yellow]")
                elif command == "/parallel":
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
                elif command.startswith("/max-tools"):
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