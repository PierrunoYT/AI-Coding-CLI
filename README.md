# AI Chat CLI

A simple command-line chat application that uses OpenRouter's API to interact with various AI models, including the latest Claude 4 models.

## Features

- Interactive chat interface
- Support for multiple AI models through OpenRouter
- Conversation history maintained during the session
- Simple and clean CLI interface
- Token usage tracking
- Support for streaming responses
- Latest Claude 4 model support

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
$env:AI_MODEL="anthropic/claude-opus-4"  # Optional, specify model

# On Linux/macOS
export OPENROUTER_API_KEY="your-api-key-here"
export APP_URL="https://your-app-url.com"  # Optional, for OpenRouter rankings
export APP_NAME="Your App Name"            # Optional, for OpenRouter rankings
export AI_MODEL="anthropic/claude-opus-4"  # Optional, specify model
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
- `AI_MODEL`: The AI model to use (optional, defaults to Claude 4 Opus)

## Available Models

OpenRouter supports various models from different providers. Here are the latest Claude 4 models:

### Claude 4 Models
- `anthropic/claude-opus-4` (Default) - Most capable model, best for complex tasks
  - Pricing: $15/M input tokens, $75/M output tokens
  - 200,000 context window
  - Best for coding, complex reasoning, and agent workflows
  - Leading performance on SWE-bench (72.5%) and Terminal-bench (43.2%)

- `anthropic/claude-sonnet-4` - Balanced performance and cost
  - Pricing: $3/M input tokens, $15/M output tokens
  - 200,000 context window
  - State-of-the-art performance on SWE-bench (72.7%)
  - Optimized for practical everyday use

### Other Popular Models
- `openai/gpt-4-turbo-preview`
- `openai/gpt-3.5-turbo`
- `google/gemini-pro`

## Model Comparison

### Claude 4 Opus
- Most capable model in the Claude 4 family
- Best for complex reasoning, analysis, and creative tasks
- Highest quality responses
- Higher cost per token
- Supports extended thinking with tool use
- Can handle thousands of task steps continuously
- Best for coding and complex problem-solving

### Claude 4 Sonnet
- Balanced performance and cost
- Good for general-purpose tasks
- Faster than Opus
- Lower cost than Opus
- Improved autonomous codebase navigation
- Reduced error rates in agent-driven workflows
- Better at following complex instructions

## License

MIT 