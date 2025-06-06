# tools.py
import os
import subprocess
import sys
from rich.console import Console

console = Console()

def list_files(directory="."):
    """Lists all files and directories in the specified directory."""
    try:
        # Handle default directory parameter
        if not directory:
            directory = "."
            
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
            [sys.executable, filename],
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

def append_to_file(filename, content):
    """Appends content to the end of a specified file."""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content)
        return f"➕ Successfully appended to {filename}."
    except Exception as e:
        return f"❌ Error appending to file: {e}"

def replace_in_file(filename, old_text, new_text):
    """Replaces all occurrences of old_text with new_text in a file."""
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist."
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text not in content:
            return f"❌ Text '{old_text}' not found in {filename}."
        
        new_content = content.replace(old_text, new_text)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        occurrences = content.count(old_text)
        return f"🔄 Successfully replaced {occurrences} occurrence(s) of '{old_text}' with '{new_text}' in {filename}."
    except Exception as e:
        return f"❌ Error replacing text in file: {e}"

def insert_line_at_position(filename, line_number, content):
    """Inserts a line at a specific position in a file (1-based line numbering)."""
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist."
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if line_number < 1 or line_number > len(lines) + 1:
            return f"❌ Invalid line number {line_number}. File has {len(lines)} lines."
        
        # Convert to 0-based indexing
        insert_index = line_number - 1
        
        # Ensure content ends with newline if it doesn't already
        if not content.endswith('\n'):
            content += '\n'
        
        lines.insert(insert_index, content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return f"📝 Successfully inserted line at position {line_number} in {filename}."
    except Exception as e:
        return f"❌ Error inserting line in file: {e}"

def read_file_lines(filename, start_line=None, end_line=None):
    """Reads specific lines from a file (1-based line numbering)."""
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist."
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        if start_line is None:
            start_line = 1
        if end_line is None:
            end_line = total_lines
        
        if start_line < 1 or end_line < 1 or start_line > total_lines:
            return f"❌ Invalid line range. File has {total_lines} lines."
        
        # Convert to 0-based indexing
        start_idx = start_line - 1
        end_idx = min(end_line, total_lines)
        
        selected_lines = lines[start_idx:end_idx]
        
        result = f"📄 Lines {start_line}-{end_idx} of {filename}:\n"
        for i, line in enumerate(selected_lines, start=start_line):
            result += f"{i:4}: {line.rstrip()}\n"
        
        return result
    except Exception as e:
        return f"❌ Error reading file lines: {e}"

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
                        "description": "The directory to inspect. Defaults to current directory if not specified."
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
    {
        "type": "function",
        "function": {
            "name": "append_to_file",
            "description": "Append content to the end of a file without overwriting existing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to append to."},
                    "content": {"type": "string", "description": "The content to append to the file."}
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "replace_in_file",
            "description": "Replace all occurrences of specific text in a file with new text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to modify."},
                    "old_text": {"type": "string", "description": "The text to find and replace."},
                    "new_text": {"type": "string", "description": "The text to replace with."}
                },
                "required": ["filename", "old_text", "new_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "insert_line_at_position",
            "description": "Insert a new line at a specific position in a file (1-based line numbering).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to modify."},
                    "line_number": {"type": "integer", "description": "The line number where to insert (1-based)."},
                    "content": {"type": "string", "description": "The content to insert."}
                },
                "required": ["filename", "line_number", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file_lines",
            "description": "Read specific lines from a file with line numbers (1-based numbering).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to read."},
                    "start_line": {"type": "integer", "description": "The starting line number (1-based). If not provided, starts from line 1."},
                    "end_line": {"type": "integer", "description": "The ending line number (1-based). If not provided, reads to end of file."}
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
    "append_to_file": append_to_file,
    "replace_in_file": replace_in_file,
    "insert_line_at_position": insert_line_at_position,
    "read_file_lines": read_file_lines,
} 