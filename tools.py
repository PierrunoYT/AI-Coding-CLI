# tools.py
import os
import subprocess
from rich.console import Console

console = Console()

def list_files(directory="."):
    """Lists all files and directories in the specified directory."""
    try:
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                items.append(f"📄 {item}")
        return "\n".join(items) if items else "Directory is empty."
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."
    except PermissionError:
        return f"Error: Permission denied accessing '{directory}'."

def write_to_file(filename, content):
    """Writes the given content to a specified file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Successfully wrote to {filename}."
    except Exception as e:
        return f"❌ Error writing to file: {e}"

def read_file(filename):
    """Reads the content of a specified file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"📄 Content of {filename}:\n{content}"
    except FileNotFoundError:
        return f"❌ Error: File '{filename}' not found."
    except Exception as e:
        return f"❌ Error reading file: {e}"

def execute_python_file(filename):
    """
    Executes a Python script and returns its output.
    **SECURITY WARNING**: This function executes code on your machine.
    Only run scripts you trust.
    """
    console.print(f"\n⚠️  [bold yellow]WARNING: About to execute Python script '{filename}'[/bold yellow]")
    console.print("[yellow]This will run code on your machine. Only proceed if you trust this script.[/yellow]")
    proceed = console.input("[bold]Continue? (y/N): [/bold]").lower().strip()
    
    if proceed != 'y':
        return "🛑 Execution cancelled by user."

    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            check=True,
            timeout=30  # 30 second timeout for safety
        )
        
        output = f"🚀 Executed {filename} successfully:\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        if not result.stdout and not result.stderr:
            output += "Script completed with no output.\n"
            
        return output
    except FileNotFoundError:
        return f"❌ Error: Script '{filename}' not found."
    except subprocess.TimeoutExpired:
        return f"⏱️ Error: Script '{filename}' timed out after 30 seconds."
    except subprocess.CalledProcessError as e:
        return f"❌ Error executing script '{filename}':\nExit code: {e.returncode}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"❌ An unexpected error occurred: {e}"

def create_directory(directory_name):
    """Creates a new directory."""
    try:
        os.makedirs(directory_name, exist_ok=True)
        return f"📁 Successfully created directory: {directory_name}"
    except Exception as e:
        return f"❌ Error creating directory: {e}"

def delete_file(filename):
    """Deletes a specified file."""
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist."
        
        console.print(f"\n⚠️  [bold red]WARNING: About to delete '{filename}'[/bold red]")
        proceed = console.input("[bold]Are you sure? (y/N): [/bold]").lower().strip()
        
        if proceed != 'y':
            return "🛑 File deletion cancelled by user."
        
        os.remove(filename)
        return f"🗑️ Successfully deleted: {filename}"
    except Exception as e:
        return f"❌ Error deleting file: {e}"

# Tool definitions for the API
TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files and directories in a given directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string", 
                        "description": "The directory to inspect. Defaults to current directory if not specified.",
                        "default": "."
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write content to a file. This will create the file if it doesn't exist or overwrite it if it does.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to write to."},
                    "content": {"type": "string", "description": "The content to write into the file."}
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full content of a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to read."}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_file",
            "description": "Execute a python script and get the output. User will be prompted for confirmation before execution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the python file to execute."}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_directory",
            "description": "Create a new directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_name": {"type": "string", "description": "The name of the directory to create."}
                },
                "required": ["directory_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a specified file. User will be prompted for confirmation before deletion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to delete."}
                },
                "required": ["filename"],
            },
        },
    },
]

# Available tools mapping
AVAILABLE_TOOLS = {
    "list_files": list_files,
    "write_to_file": write_to_file,
    "read_file": read_file,
    "execute_python_file": execute_python_file,
    "create_directory": create_directory,
    "delete_file": delete_file,
} 