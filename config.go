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

	// Default to Claude 4 Opus, the most capable model
	model := os.Getenv("AI_MODEL")
	if model == "" {
		model = "anthropic/claude-opus-4" // Latest Claude 4 model
	}

	return &Config{
		OpenRouterAPIKey: apiKey,
		Model:            model,
		AppURL:           appURL,
		AppName:          appName,
	}, nil
} 