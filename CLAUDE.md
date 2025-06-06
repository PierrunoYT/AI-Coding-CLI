# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Test API connection before development
python test_api.py

# Run the main application
python main.py

# Enable debug mode for development
export DEBUG=true
python main.py
```

### Environment Setup
```bash
# Required: Set OpenRouter API key
export OPENROUTER_API_KEY="sk-or-your-api-key-here"

# Optional: Development variables
export APP_URL="https://your-app-url.com"
export APP_NAME="Your App Name" 
export DEBUG="true"
```

## Architecture Overview

This is a CLI chat application with a dual-mode architecture: regular chat and coding agent mode with file system tools.

### Core Components

**Config Class** (`main.py`):
- Centralized configuration management
- Environment variable handling
- Agent mode and tool execution settings
- Model selection and compatibility tracking

**ChatClient Class** (`main.py`):
- OpenRouter API integration with full conversation management
- Error handling with automatic retry mechanisms (especially for 400 errors)
- Tool execution orchestration (sequential vs parallel modes)
- Smart tool promise detection system that catches when AI says it will use tools but doesn't

**Tool System** (`tools.py`):
- 10 file system tools with OpenAI-compatible function definitions
- Safety confirmations for destructive operations (delete, execute)
- Comprehensive error handling and input validation

### Key Architectural Patterns

**Conversation Flow Management**:
- System messages are injected for agent mode
- Conversation history is carefully managed to prevent duplicates during tool retry scenarios
- Tool execution results are integrated back into conversation context

**Error Recovery Strategy**:
- API errors trigger automatic retries without `tool_choice` parameter
- Undefined response variables are handled with proper null checks
- Model compatibility is detected and warnings are shown

**Tool Execution Modes**:
- Sequential: Tools run one after another with progress tracking
- Parallel: Uses ThreadPoolExecutor for concurrent execution with progress bars
- Configurable limits (1-20 tools per response) for safety

## Development Notes

### Documentation Requirements
**CRITICAL**: Always update these files when making changes AND commit them:
- `README.md` - User-facing documentation  
- `tasks.md` - Development history and technical details
- `project-structure.md` - When file structure changes
- `code-issues.md` - When fixing bugs or adding new issues

**Required Workflow**:
1. Make code changes
2. Update all relevant markdown files listed above
3. Commit ALL changes together with descriptive commit message
4. Use conventional commit format: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, or `build:`
5. Include Claude Code attribution in commit message

### Critical Code Areas

**Conversation History Management** (`main.py:327`):
- AI messages must only be added to history in appropriate conditional blocks
- Avoid duplicate messages during tool retry scenarios

**Error Handling** (`main.py:72-91`):
- Always initialize response variables before try blocks
- Include null checks before accessing response attributes
- Provide fallback error messages

**Python Script Execution** (`tools.py:59`):
- Use `sys.executable` instead of hardcoded "python" for cross-platform compatibility
- Ensure script execution works regardless of how Python is installed (python vs python3)

**Tool Execution** (`main.py:378-452`):
- Tool calls are limited for safety (configurable 1-20 per response)
- Results must be sorted by original order in parallel mode
- Each tool result includes execution timing and error details

### Model Compatibility
Function calling support is detected via hardcoded patterns in `main.py:158`. Supported models include:
- OpenAI: gpt-4, gpt-3.5-turbo variants
- Anthropic: claude-3 series
- Google: gemini-pro, gemini-1.5-pro

### Testing Strategy
- Use `test_api.py` for API connectivity validation
- Manual testing required for tool execution modes
- Test error conditions with invalid API keys/models
- Verify tool promise detection with various AI response patterns

### Commit Message Template
```
<type>: <description>

- <change 1>
- <change 2>
- Updated documentation files as required

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```