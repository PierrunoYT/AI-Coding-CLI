package main

import (
	"fmt"
	"os"
)

type Config struct {
	OpenRouterAPIKey string
	Model            string
	AppURL           string
	AppName          string
}

// Latest OpenAI Models (2024-2025) - Top performing models
const (
	// GPT-4.1 Series (Latest flagship models - April 2025)
	GPT41          = "openai/gpt-4.1"          // Flagship model with 1M context, excellent for coding
	GPT41Mini      = "openai/gpt-4.1-mini"     // Smaller version of GPT-4.1
	GPT41Nano      = "openai/gpt-4.1-nano"     // Ultra-fast, cost-efficient variant
	
	// GPT-4 Series (Previous generation)
	GPT4Turbo      = "openai/gpt-4-turbo-preview"  // GPT-4 Turbo
	GPT4Vision     = "openai/gpt-4-vision-preview" // GPT-4 with vision capabilities
	GPT4           = "openai/gpt-4"                // Standard GPT-4
	
	// GPT-3.5 Series (Fast and efficient)
	GPT35Turbo     = "openai/gpt-3.5-turbo"        // Latest GPT-3.5 Turbo
	GPT35Turbo16K  = "openai/gpt-3.5-turbo-16k"    // GPT-3.5 with 16K context
	
	// Legacy Claude models (keeping for backward compatibility)
	ClaudeOpus4     = "anthropic/claude-opus-4"
	ClaudeSonnet4   = "anthropic/claude-sonnet-4"
	ClaudeSonnet35  = "anthropic/claude-3.5-sonnet"
	ClaudeSonnet37  = "anthropic/claude-3.7-sonnet"
)

// Top 5 OpenAI Models by Performance
const (
	// 1. GPT-4.1 - Best overall performance
	TopModel1 = GPT41
	
	// 2. GPT-4 Turbo - Best for complex tasks
	TopModel2 = GPT4Turbo
	
	// 3. GPT-4 Vision - Best for multimodal tasks
	TopModel3 = GPT4Vision
	
	// 4. GPT-3.5 Turbo - Best for general tasks
	TopModel4 = GPT35Turbo
	
	// 5. GPT-3.5 Turbo 16K - Best for longer context
	TopModel5 = GPT35Turbo16K
)

func LoadConfig() (*Config, error) {
	apiKey := os.Getenv("OPENROUTER_API_KEY")
	if apiKey == "" {
		return nil, fmt.Errorf("OPENROUTER_API_KEY environment variable is not set")
	}

	appURL := os.Getenv("APP_URL")
	if appURL == "" {
		appURL = "https://github.com/yourusername/aichat" // Default value
	}

	appName := os.Getenv("APP_NAME")
	if appName == "" {
		appName = "AI Chat CLI" // Default value
	}

	// Default to GPT-4.1, the latest flagship model with best coding capabilities
	model := os.Getenv("AI_MODEL")
	if model == "" {
		model = GPT41 // Default to the latest and most capable model
	}

	return &Config{
		OpenRouterAPIKey: apiKey,
		Model:            model,
		AppURL:           appURL,
		AppName:          appName,
	}, nil
} 