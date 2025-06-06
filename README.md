# AI Chat CLI (Python)

A powerful command-line chat application that uses OpenRouter's API to interact with various AI models. Features both regular chat and coding agent modes for enhanced productivity.

## Recent Updates

### 🆕 Latest Features & Fixes (January 2025)
- **🔧 Enhanced Code Quality**: Fixed 4 high/medium priority issues including model compatibility detection, exception handling, schema compliance, and repository URL
- **✅ Fixed AI Response Labeling**: AI responses now properly display with "AI:" label instead of just showing "you:"
- **🎯 Smart Tool Promise Detection**: Automatically detects when AI promises to use tools but doesn't follow through
- **⚡ Parallel Tool Execution**: Run multiple tools simultaneously for faster operation
- **🛡️ Enhanced Error Recovery**: Improved handling of API errors with automatic retries
- **🔧 Model Compatibility Checks**: Better detection and warnings for models that don't support function calling

## Features

- **Interactive Chat Interface**: Rich text UI powered by `rich` library
- **Coding Agent Mode**: AI assistant with file system tools for development tasks
- **Universal Model Support**: Access to all AI models available through OpenRouter
- **Dynamic Model Selection**: Choose from a filterable list of available models
- **File System Operations**: List, read, write, and manage files and directories
- **Code Execution**: Run Python scripts with safety confirmations
- **Smart Tool Promise Detection**: Automatically detects when AI promises to use tools but doesn't follow through
- **Conversation History**: Maintained during the session with full context
- **Token Usage Tracking**: Monitor API usage and statistics
- **Intuitive Commands**: Simple CLI interface with helpful commands
- **Robust Error Handling**: Graceful handling of API errors with automatic retries
- **Connection Testing**: Automatic API connectivity validation on startup
- **Model Compatibility Checks**: Warns about models that don't support function calling
- **Debug Mode**: Detailed logging for troubleshooting API issues

## Prerequisites

- Python 3.7+
- An OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/aichat-py.git
   cd aichat-py
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenRouter API key:**

   **Windows PowerShell:**
   ```powershell
   $env:OPENROUTER_API_KEY="sk-or-your-api-key-here"
   ```

   **Linux/macOS:**
   ```bash
   export OPENROUTER_API_KEY="sk-or-your-api-key-here"
   ```

   **Optional environment variables:**
   ```bash
   export APP_URL="https://your-app-url.com"     # Optional: Your app URL for OpenRouter
   export APP_NAME="Your App Name"               # Optional: Custom app name
   export DEBUG="true"                           # Optional: Enable debug logging
   ```

4. **Test your setup (recommended):**
   ```bash
   python test_api.py
   ```
   This will verify your API key and connection before running the main application.

5. **Run the application:**
   ```bash
   python main.py
   ```

## Quick Start

1. Run `python main.py`
2. Type `/agent` to enable coding agent mode
3. Try: "List the files in the current directory"
4. Type `/help` for all available commands

## Available Commands

### Core Commands
- `/help` - Show available commands and agent mode information
- `/model` - Show current model information  
- `/models` - List and select from all available OpenRouter models
- `/stats` - Show conversation statistics
- `/reset` - Reset conversation history
- `/clear` - Clear the screen
- `/exit` - Exit the application

### Agent Mode Commands
- `/agent` - Toggle coding agent mode (enables file system tools)
- `/parallel` - Toggle tool execution mode (parallel/sequential)
- `/max-tools <number>` - Set maximum tool calls per response (1-20)

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
- **Sequential Mode** 🔄: Tools run one after another (default)
  - Safer for dependent operations
  - Shows step-by-step progress
  - Better for file operations that depend on each other
- **Parallel Mode** ⚡: Multiple tools run simultaneously  
  - Faster execution for independent operations
  - Progress bar shows completion status
  - Perfect for bulk file operations

### Smart Tool Promise Detection 🎯
The CLI now automatically detects when the AI says it will use a tool (like "let me check the files" or "I'll read that file") but doesn't actually call the function. When this happens:
- You'll see a warning message highlighting the oversight
- You can choose to ask the AI to follow through with its promise
- This helps ensure the AI actually performs the actions it describes

### Example Agent Tasks

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

## Model Selection & Compatibility

The application supports dynamic model selection from all available OpenRouter models.

### Selecting a Model
1. Type `/models` to see the list of available models
2. Each model shows its ID, context length, and pricing information
3. Select a model by:
   - Entering the number from the list, or
   - Typing the model handle directly (e.g., `openai/gpt-4o`)

### Function Calling Support
For agent mode to work properly, use models that support function calling:
- ✅ **Recommended**: `openai/gpt-4o`, `openai/gpt-4`, `openai/gpt-3.5-turbo`
- ✅ **Good**: `anthropic/claude-3-5-sonnet`, `anthropic/claude-3-haiku`
- ✅ **Supported**: `google/gemini-pro`, `google/gemini-1.5-pro`
- ⚠️ **Limited**: Other models may not support function calling

The application will automatically detect and warn you if your selected model doesn't support function calling.

## Troubleshooting

### Common Issues

**1. "OPENROUTER_API_KEY environment variable not set"**
- Solution: Set your API key using the commands in the Setup section
- Make sure your key starts with `sk-or-` (OpenRouter keys)

**2. "Authentication failed" or 401 errors**
- Check that your API key is correct and active
- Verify your OpenRouter account has sufficient credits
- Run `python test_api.py` to test your API key

**3. "400 Bad Request" errors**
- The application now handles these automatically with retry logic
- If problems persist, try switching to a different model with `/models`
- Enable debug mode: `export DEBUG=true` and run again

**4. "Tool choice parameter causing issues"**
- This is handled automatically - the app will retry without tool_choice
- Consider switching to a function-calling compatible model

**5. Model doesn't support function calling**
- Switch to a recommended model (see Model Compatibility section)
- Agent mode features won't work with non-compatible models

### Debug Mode

Enable detailed logging for troubleshooting:
```bash
export DEBUG=true
python main.py
```

This will show:
- API request details
- Model compatibility checks
- Detailed error messages
- Tool execution information

### Testing Your Setup

Use the included test script to verify everything works:
```bash
python test_api.py
```

This will:
- ✅ Check if your API key is set
- ✅ Test connection to OpenRouter
- ✅ Verify authentication
- ✅ Show how many models are available

## Advanced Configuration

### Environment Variables
```bash
OPENROUTER_API_KEY="sk-or-your-key"     # Required: Your OpenRouter API key
APP_URL="https://your-site.com"         # Optional: For OpenRouter attribution
APP_NAME="Your App Name"                # Optional: Custom app name
DEBUG="true"                            # Optional: Enable debug logging
```

### Safety Features
- **Confirmation prompts**: For file deletion and code execution
- **Timeout protection**: Python scripts are limited to 30 seconds
- **Tool call limits**: Maximum 10 tools per response (configurable)
- **Error recovery**: Automatic retry logic for common API issues

## Files in This Project

- `main.py` - Main application with chat interface and agent mode
- `tools.py` - File system tools and function definitions
- `test_api.py` - API connection testing utility
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `CLAUDE.md` - Development guidance for Claude Code instances
- `code-issues.md` - Code quality analysis and issue tracking
- `tasks.md` - Complete development history and technical documentation
- `project-structure.md` - Architecture overview and file structure

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

If you encounter issues:
1. Run `python test_api.py` to test your setup
2. Enable debug mode with `DEBUG=true`
3. Check the troubleshooting section above
4. Open an issue with your error details

## 🌐 Deployment Status

✅ **Repository Successfully Created and Deployed**
- GitHub Repository: https://github.com/PierrunoYT/AI-Coding-CLI
- All files pushed to main branch
- Ready for installation and usage

## 📋 Task Completion Status

✅ All tasks completed successfully:
- ✅ Fixed 400 Bad Request API errors
- ✅ Implemented robust error handling and retry mechanisms  
- ✅ Added comprehensive API validation and debugging features
- ✅ Created complete documentation ecosystem
- ✅ Set up GitHub repository and deployment
- ✅ Updated all required documentation files per workspace rules

**Project Status**: Production Ready 🚀 