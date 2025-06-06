# AI Chat CLI (Python)

A powerful command-line chat application that uses OpenRouter's API to interact with various AI models. Features both regular chat and coding agent modes for enhanced productivity.

## Features

- **Interactive Chat Interface**: Rich text UI powered by `rich` library
- **Coding Agent Mode**: AI assistant with file system tools for development tasks
- **Universal Model Support**: Access to all AI models available through OpenRouter
- **Dynamic Model Selection**: Choose from a filterable list of available models
- **File System Operations**: List, read, write, and manage files and directories
- **Code Execution**: Run Python scripts with safety confirmations
- **Conversation History**: Maintained during the session with full context
- **Token Usage Tracking**: Monitor API usage and statistics
- **Intuitive Commands**: Simple CLI interface with helpful commands

## Prerequisites

- Python 3.7+
- An OpenRouter API key

## Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/aichat-py.git
    cd aichat-py
    ```

2.  Set your environment variables. You can create a `.env` file or set them directly in your shell.
    ```bash
    # On Windows PowerShell
    $env:OPENROUTER_API_KEY="your-api-key-here"
    $env:APP_URL="https://your-app-url.com"  # Optional
    $env:APP_NAME="Your App Name"            # Optional

    # On Linux/macOS
    export OPENROUTER_API_KEY="your-api-key-here"
    export APP_URL="https://your-app-url.com"  # Optional
    export APP_NAME="Your App Name"            # Optional
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application:
```bash
python main.py
```

- Type your message and press Enter to send.
- Type `/help` to see a list of available commands.

## Available Commands

- `/help` - Show available commands and agent mode information
- `/model` - Show current model information
- `/models` - List and select from all available OpenRouter models
- `/agent` - Toggle coding agent mode (enables file system tools)
- `/parallel` - Toggle tool execution mode (parallel/sequential)
- `/max-tools <number>` - Set maximum tool calls per response (1-20)
- `/stats` - Show conversation statistics
- `/reset` - Reset conversation history
- `/clear` - Clear the screen
- `/exit` - Exit the application

## Coding Agent Mode

Enable powerful coding assistance by typing `/agent` to toggle agent mode. When enabled, the AI assistant has access to these tools:

### File Operations
- **List Files**: Browse directories and see file structure
- **Read Files**: View file contents or specific line ranges
- **Write Files**: Create new files or completely overwrite existing ones
- **Edit Files**: Advanced editing capabilities:
  - **Append**: Add content to the end of files
  - **Replace**: Find and replace text throughout files
  - **Insert**: Add lines at specific positions
- **Delete Files**: Remove files (with confirmation)

### Directory Operations
- **Create Directories**: Make new folders for project organization

### Code Execution
- **Run Python Scripts**: Execute Python files with safety confirmations and timeout protection

### Tool Execution Modes
- **Sequential Mode** 🔄: Tools run one after another
  - Safer for dependent operations
  - Shows step-by-step progress
  - Better for file operations that depend on each other
- **Parallel Mode** ⚡: Multiple tools run simultaneously  
  - Faster execution for independent operations
  - Progress bar shows completion status
  - Perfect for bulk file operations

### Example Agent Tasks
Try these commands in agent mode:

**Basic Operations:**
- "List the files in the current directory"
- "Create a Python script that prints 'Hello World' and save it as hello.py"
- "Read the contents of main.py"
- "Execute the hello.py script"
- "Create a new directory called 'projects'"

**Advanced Editing:**
- "Read lines 1-10 of main.py"
- "Append a comment to the end of hello.py"
- "Replace 'Hello World' with 'Hello Coding Agent' in hello.py"
- "Insert a new import statement at line 2 in main.py"

**Bulk Operations (perfect for parallel mode):**
- "Create three Python files: app.py, utils.py, and config.py"
- "Read the contents of all .py files in this directory"
- "Backup all important files by creating .bak copies"

**Configuration Commands:**
- `/parallel` - Switch between sequential and parallel tool execution
- `/max-tools 15` - Allow up to 15 tool calls per AI response

## Model Selection

The application supports dynamic model selection from all available OpenRouter models.

1.  Type `/models` to see the list of available models.
2.  Each model will show its ID, context length, and pricing information.
3.  You can select a model in two ways:
    -   Enter the number of the model from the list.
    -   Type the model handle directly (e.g., `openai/gpt-4o`).
4.  The selected model will be used for all subsequent conversations.

## License

MIT 