# AI Chat CLI

A simple command-line chat application that uses OpenRouter's API to interact with various AI models, including the latest GPT-4.1 and Claude models.

## Features

- Interactive chat interface
- Support for multiple AI models through OpenRouter
- Dynamic model selection from all available OpenRouter models
- Conversation history maintained during the session
- Simple and clean CLI interface
- Token usage tracking
- Support for streaming responses
- Latest GPT-4.1 and Claude model support

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

## Available Commands

- `help` - Show available commands
- `model` - Show current model information
- `models` - List and select from all available OpenRouter models
- `stats` - Show conversation statistics
- `reset` - Reset conversation history
- `clear` - Clear the screen
- `exit` - Exit the application

## Model Selection

The application supports dynamic model selection from all available OpenRouter models. To change models:

1. Type `models` to see the list of available models
2. Each model will show:
   - Model ID
   - Name
   - Context length
   - Pricing information
   - Description (if available)
3. Enter the number of the model you want to use
4. The selected model will be used for all subsequent conversations

## Configuration

The following environment variables can be configured:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `APP_URL`: Your application's URL (optional, for OpenRouter rankings)
- `APP_NAME`: Your application's name (optional, for OpenRouter rankings)

## Top 5 OpenAI Models

Based on OpenRouter rankings and performance metrics, here are the top 5 OpenAI models:

1. **GPT-4.1** (`openai/gpt-4.1`)
   - Best overall performance
   - 1,047,576 context window
   - Pricing: $2/M input, $8/M output
   - Best for: Advanced coding, long-context reasoning
   - Performance: 54.6% SWE-bench, 87.4% IFEval

2. **GPT-4 Turbo** (`openai/gpt-4-turbo-preview`)
   - Best for complex tasks
   - 128K context window
   - Pricing: $10/M input, $30/M output
   - Best for: Complex analysis, coding
   - High performance on general tasks

3. **GPT-4 Vision** (`openai/gpt-4-vision-preview`)
   - Best for multimodal tasks
   - 128K context window
   - Pricing: $10/M input, $30/M output
   - Best for: Image analysis, multimodal understanding
   - Excellent visual reasoning capabilities

4. **GPT-3.5 Turbo** (`openai/gpt-3.5-turbo`)
   - Best for general tasks
   - 16K context window
   - Pricing: $0.5/M input, $1.5/M output
   - Best for: Quick responses, general queries
   - Cost-effective for most use cases

5. **GPT-3.5 Turbo 16K** (`openai/gpt-3.5-turbo-16k`)
   - Best for longer context
   - 16K context window
   - Pricing: $0.5/M input, $1.5/M output
   - Best for: Longer conversations, document analysis
   - Extended context at same cost

## Available Models

OpenRouter supports various models from different providers. Here are the available models:

### GPT-4.1 Series (Latest - April 2025)
- `openai/gpt-4.1` (Default) - Flagship model
  - Pricing: $2/M input tokens, $8/M output tokens
  - 1,047,576 context window
  - Best for advanced coding and long-context reasoning
  - 54.6% SWE-bench Verified, 87.4% IFEval
  - Optimized for software engineering and agent reliability

- `openai/gpt-4.1-mini` - Smaller version
  - Pricing: Lower than GPT-4.1
  - 1M context window
  - Balanced performance and cost
  - Good for general-purpose tasks

- `openai/gpt-4.1-nano` - Fastest version
  - Pricing: Most cost-effective
  - 1M context window
  - Best for quick responses and basic tasks

### GPT-4 Series
- `openai/gpt-4-turbo-preview`
  - Pricing: $10/M input tokens, $30/M output tokens
  - 128K context window
  - Best for complex tasks and analysis

- `openai/gpt-4-vision-preview`
  - Pricing: $10/M input tokens, $30/M output tokens
  - 128K context window
  - Best for image analysis and multimodal tasks

### GPT-3.5 Series
- `openai/gpt-3.5-turbo`
  - Pricing: $0.5/M input tokens, $1.5/M output tokens
  - 16K context window
  - Best for general tasks and quick responses

### Claude Models
- `anthropic/claude-opus-4`
  - Pricing: $15/M input tokens, $75/M output tokens
  - 200,000 context window
  - Best for complex reasoning and coding

- `anthropic/claude-sonnet-4`
  - Pricing: $3/M input tokens, $15/M output tokens
  - 200,000 context window
  - Best for balanced performance

## Model Comparison

### GPT-4.1 (Default)
- Latest flagship model with 1M+ context window
- Best for advanced coding and long-context reasoning
- Excellent performance on SWE-bench (54.6%)
- High instruction compliance (87.4% IFEval)
- Optimized for software engineering
- Competitive pricing at $2/M input, $8/M output

### GPT-4.1 Mini
- Smaller version of GPT-4.1
- Same 1M context window
- Lower cost than flagship model
- Good balance of performance and cost
- Suitable for most general tasks

### GPT-4.1 Nano
- Fastest and most cost-effective variant
- Same 1M context window
- Best for quick responses
- Ideal for basic tasks and simple queries

### GPT-4 Turbo
- Previous generation model
- 128K context window
- Higher cost than GPT-4.1
- Good for complex tasks and analysis
- Supports vision capabilities

### GPT-3.5 Turbo
- Fast and cost-effective
- 16K context window
- Best for general tasks
- Quick response times
- Lowest cost option

### Claude Opus 4
- High-performance model
- 200K context window
- Best for complex reasoning
- Higher cost than GPT-4.1
- Good for coding tasks

### Claude Sonnet 4
- Balanced performance
- 200K context window
- Moderate cost
- Good for general-purpose tasks
- Reliable performance

## License

MIT 