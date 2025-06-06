# AI Chat CLI

A simple command-line chat application that uses OpenRouter's API to interact with various AI models.

## Features

- Interactive chat interface
- Support for multiple AI models through OpenRouter
- Conversation history maintained during the session
- Simple and clean CLI interface
- Token usage tracking
- Support for streaming responses (coming soon)

## Prerequisites

- Go 1.21 or later
- OpenRouter API key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aichat.git
cd aichat
```

2. Set your environment variables:
```bash
# On Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key-here"
$env:APP_URL="https://your-app-url.com"  # Optional, for OpenRouter rankings
$env:APP_NAME="Your App Name"            # Optional, for OpenRouter rankings

# On Linux/macOS
export OPENROUTER_API_KEY="your-api-key-here"
export APP_URL="https://your-app-url.com"  # Optional, for OpenRouter rankings
export APP_NAME="Your App Name"            # Optional, for OpenRouter rankings
```

3. Install dependencies:
```bash
go mod download
```

## Usage

Run the application:
```bash
go run .
```

- Type your message and press Enter to send
- Type 'exit' to quit the application

## Configuration

The following environment variables can be configured:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `APP_URL`: Your application's URL (optional, for OpenRouter rankings)
- `APP_NAME`: Your application's name (optional, for OpenRouter rankings)

The default model is set to "anthropic/claude-3-opus-20240229". You can modify this in the `config.go` file.

## Available Models

OpenRouter supports various models from different providers. Some popular options include:

- `anthropic/claude-3-opus-20240229`
- `anthropic/claude-3-sonnet-20240229`
- `openai/gpt-4-turbo-preview`
- `openai/gpt-3.5-turbo`
- `google/gemini-pro`

## License

MIT 