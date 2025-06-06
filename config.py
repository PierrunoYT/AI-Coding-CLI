import os

class Config:
    """Centralized configuration management for the AI Chat CLI application."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.app_url = os.getenv("APP_URL", "https://github.com/PierrunoYT/ai-coding-cli")
        self.app_name = os.getenv("APP_NAME", "AI Chat CLI (Python)")
        self.default_model = "openai/gpt-4o"
        self.model = self.default_model
        self.agent_mode = False  # Toggle for coding agent mode
        self.tool_execution_mode = "sequential"  # "sequential" or "parallel"
        self.max_tool_calls = 10  # Maximum tool calls per response
        self.debug = os.getenv("DEBUG", "false").lower() == "true"  # Debug mode

    def get_model(self):
        """Get the current model."""
        return self.model

    def set_model(self, model_id):
        """Set the current model."""
        self.model = model_id
    
    def toggle_agent_mode(self):
        """Toggle agent mode on/off and return the new state."""
        self.agent_mode = not self.agent_mode
        return self.agent_mode
    
    def toggle_tool_execution_mode(self):
        """Toggle between sequential and parallel tool execution modes."""
        if self.tool_execution_mode == "sequential":
            self.tool_execution_mode = "parallel"
        else:
            self.tool_execution_mode = "sequential"
        return self.tool_execution_mode
    
    def set_max_tool_calls(self, max_calls):
        """Set the maximum number of tool calls per response (1-20)."""
        if max_calls > 0 and max_calls <= 20:
            self.max_tool_calls = max_calls
            return True
        return False