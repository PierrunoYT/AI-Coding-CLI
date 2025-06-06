# AI Chat CLI (Python)

A simple command-line chat application that uses OpenRouter's API to interact with various AI models. This is a Python port of the original Go project.

## Features

- Interactive chat interface with rich text, powered by `rich`
- Support for all AI models available through OpenRouter
- Dynamic model selection from a filterable list
- Streaming responses for instant interaction
- Conversation history maintained during the session
- Token usage and statistics tracking
- Simple and clean CLI interface with intuitive commands

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

- `/help` - Show available commands
- `/model` - Show current model information
- `/models` - List and select from all available OpenRouter models
- `/stats` - Show conversation statistics
- `/reset` - Reset conversation history
- `/clear` - Clear the screen
- `/exit` - Exit the application

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