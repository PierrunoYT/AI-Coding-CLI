package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/fatih/color"
)

// Global config variable
var config *Config

// Enhanced stats structure
type EnhancedChatStats struct {
	MessageCount        int
	TotalTokens        int
	PromptTokens       int
	CompletionTokens   int
	AverageResponseTime float64
	StartTime          time.Time
}

func printWelcome() {
	// Clear screen
	fmt.Print("\033[H\033[2J")

	// Print welcome message with colors
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("╔════════════════════════════════════════════════════════════╗"))
	fmt.Printf("%s\n", cyan("║                     AI Chat CLI v1.0                        ║"))
	fmt.Printf("%s\n", cyan("╚════════════════════════════════════════════════════════════╝"))
	fmt.Printf("\n%s %s\n", yellow("Model:"), green(config.Model))
	fmt.Printf("%s %s\n", yellow("Provider:"), green("OpenRouter"))
	fmt.Printf("%s %s\n", yellow("Type 'exit' to quit, 'clear' to clear screen, 'help' for commands"))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printHelp() {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("Available Commands:"))
	fmt.Printf("%s %s\n", yellow("• exit"), green("- Exit the application"))
	fmt.Printf("%s %s\n", yellow("• clear"), green("- Clear the screen"))
	fmt.Printf("%s %s\n", yellow("• help"), green("- Show this help message"))
	fmt.Printf("%s %s\n", yellow("• model"), green("- Show current model information"))
	fmt.Printf("%s %s\n", yellow("• models"), green("- List and select available models"))
	fmt.Printf("%s %s\n", yellow("• stats"), green("- Show conversation statistics"))
	fmt.Printf("%s %s\n", yellow("• reset"), green("- Reset conversation history"))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printModelInfo() {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("Model Information:"))
	fmt.Printf("%s %s\n", yellow("• Current Model:"), green(config.Model))
	
	// Display model-specific information based on the model name
	switch {
	case strings.Contains(config.Model, "gpt-4.1"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("1,047,576 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$2/M input, $8/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Advanced coding, long-context reasoning"))
		fmt.Printf("%s %s\n", yellow("• Features:"), green("54.6% SWE-bench Verified, 87.4% IFEval"))
	case strings.Contains(config.Model, "gpt-4.1-mini"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("1M tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("Lower than GPT-4.1"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Balanced performance and cost"))
	case strings.Contains(config.Model, "gpt-4.1-nano"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("1M tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("Most cost-effective"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Fast responses, basic tasks"))
	case strings.Contains(config.Model, "gpt-4-turbo"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("128K tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$10/M input, $30/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Complex tasks, coding, analysis"))
	case strings.Contains(config.Model, "gpt-4-vision"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("128K tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$10/M input, $30/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Image analysis, multimodal tasks"))
	case strings.Contains(config.Model, "gpt-3.5-turbo"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("16K tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$0.5/M input, $1.5/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("General tasks, quick responses"))
	case strings.Contains(config.Model, "claude-opus-4"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$15/M input, $75/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Complex reasoning, coding"))
	case strings.Contains(config.Model, "claude-sonnet-4"):
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$3/M input, $15/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Balanced performance"))
	default:
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("Varies by model"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("Check OpenRouter for details"))
	}
	
	fmt.Printf("%s %s\n", yellow("• Streaming:"), green("Enabled"))
	fmt.Printf("%s %s\n", yellow("• Provider:"), green("OpenRouter"))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printStats(stats *EnhancedChatStats) {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	sessionTime := time.Since(stats.StartTime)
	
	fmt.Printf("\n%s\n", cyan("Conversation Statistics:"))
	fmt.Printf("%s %s\n", yellow("• Messages:"), green(fmt.Sprintf("%d", stats.MessageCount)))
	fmt.Printf("%s %s\n", yellow("• Total Tokens:"), green(fmt.Sprintf("%d", stats.TotalTokens)))
	fmt.Printf("%s %s\n", yellow("• Prompt Tokens:"), green(fmt.Sprintf("%d", stats.PromptTokens)))
	fmt.Printf("%s %s\n", yellow("• Completion Tokens:"), green(fmt.Sprintf("%d", stats.CompletionTokens)))
	fmt.Printf("%s %s\n", yellow("• Average Response Time:"), green(fmt.Sprintf("%.2fs", stats.AverageResponseTime)))
	fmt.Printf("%s %s\n", yellow("• Session Duration:"), green(fmt.Sprintf("%.0f minutes", sessionTime.Minutes())))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printModelList(models []ModelInfo) {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("Available Models:"))
	for i, model := range models {
		fmt.Printf("%s %s\n", yellow(fmt.Sprintf("%d.", i+1)), green(model.ID))
		fmt.Printf("   %s %s\n", yellow("• Name:"), green(model.Name))
		fmt.Printf("   %s %s\n", yellow("• Context:"), green(fmt.Sprintf("%d tokens", model.ContextLength)))
		fmt.Printf("   %s %s\n", yellow("• Pricing:"), green(fmt.Sprintf("$%s/M input, $%s/M output", 
			model.Pricing.Prompt, model.Pricing.Completion)))
		if model.Description != "" {
			fmt.Printf("   %s %s\n", yellow("• Description:"), green(model.Description))
		}
		fmt.Println()
	}
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func selectModel(chatClient *ChatClient) error {
	models, err := chatClient.GetAvailableModels()
	if err != nil {
		return fmt.Errorf("failed to get models: %v", err)
	}

	fmt.Println("\nAvailable Models:")
	printModelList(models)

	fmt.Println("\nEnter model number or type model handle (e.g., 'openai/gpt-4-0314'):")
	var input string
	fmt.Scanln(&input)

	// Try to parse as number first
	if num, err := strconv.Atoi(input); err == nil {
		if num < 1 || num > len(models) {
			return fmt.Errorf("invalid model number")
		}
		selectedModel := models[num-1]
		config.SetModel(selectedModel.ID)
		fmt.Printf("\nSelected model: %s\n", selectedModel.ID)
		return nil
	}

	// If not a number, treat as model handle
	// Validate that the model exists in the list
	for _, model := range models {
		if model.ID == input {
			config.SetModel(input)
			fmt.Printf("\nSelected model: %s\n", input)
			return nil
		}
	}

	return fmt.Errorf("invalid model handle: %s", input)
}

func main() {
	var err error
	config, err = LoadConfig()
	if err != nil {
		red := color.New(color.FgRed).SprintFunc()
		fmt.Printf("%s Error loading configuration: %v\n", red("✗"), err)
		fmt.Printf("\n%s\n", color.New(color.FgYellow).Sprint("Make sure to set your OPENROUTER_API_KEY environment variable:"))
		fmt.Printf("%s\n", color.New(color.FgCyan).Sprint("• Windows: $env:OPENROUTER_API_KEY=\"your-key-here\""))
		fmt.Printf("%s\n", color.New(color.FgCyan).Sprint("• Linux/macOS: export OPENROUTER_API_KEY=\"your-key-here\""))
		os.Exit(1)
	}

	chatClient := NewChatClient(config)
	stats := &EnhancedChatStats{
		StartTime: time.Now(),
	}

	printWelcome()

	reader := bufio.NewReader(os.Stdin)
	for {
		// Print prompt with color
		cyan := color.New(color.FgCyan).SprintFunc()
		fmt.Printf("\n%s ", cyan("You >"))

		// Read user input
		input, err := reader.ReadString('\n')
		if err != nil {
			red := color.New(color.FgRed).SprintFunc()
			fmt.Printf("%s Error reading input: %v\n", red("✗"), err)
			continue
		}

		// Trim whitespace and check for exit command
		input = strings.TrimSpace(input)
		if input == "exit" {
			green := color.New(color.FgGreen).SprintFunc()
			fmt.Printf("\n%s Thanks for using AI Chat CLI!\n", green("✓"))
			fmt.Printf("%s Final stats: %d messages, %d tokens, %.1f minutes\n", 
				color.New(color.FgCyan).Sprint("📊"), 
				stats.MessageCount, 
				stats.TotalTokens, 
				time.Since(stats.StartTime).Minutes())
			break
		}

		// Handle special commands
		switch input {
		case "clear":
			printWelcome()
			continue
		case "help":
			printHelp()
			continue
		case "model":
			printModelInfo()
			continue
		case "models":
			if err := selectModel(chatClient); err != nil {
				red := color.New(color.FgRed).SprintFunc()
				fmt.Printf("\n%s %v\n", red("✗ Error:"), err)
			}
			continue
		case "stats":
			printStats(stats)
			continue
		case "reset":
			chatClient = NewChatClient(config)
			stats = &EnhancedChatStats{StartTime: time.Now()}
			green := color.New(color.FgGreen).SprintFunc()
			fmt.Printf("\n%s Conversation history reset!\n", green("✓"))
			continue
		case "":
			continue
		}

		// Get response from AI
		startTime := time.Now()
		response, err := chatClient.GetResponse(input)
		responseTime := time.Since(startTime)
		
		if err != nil {
			red := color.New(color.FgRed).SprintFunc()
			fmt.Printf("\n%s %v\n", red("✗ Error:"), err)
			
			// Check if it's an authentication error
			if strings.Contains(err.Error(), "401") || strings.Contains(err.Error(), "authentication") {
				fmt.Printf("%s Check your OPENROUTER_API_KEY environment variable\n", red("  →"))
			} else if strings.Contains(err.Error(), "429") {
				fmt.Printf("%s Rate limit exceeded. Please wait and try again\n", red("  →"))
			}
			continue
		}

		// Update comprehensive statistics
		stats.MessageCount++
		// Note: In a real implementation, we'd get actual token counts from the API response
		// For now, we'll estimate based on word count
		estimatedTokens := len(strings.Fields(input)) + len(strings.Fields(response))
		stats.TotalTokens += estimatedTokens
		stats.PromptTokens += len(strings.Fields(input))
		stats.CompletionTokens += len(strings.Fields(response))
		stats.AverageResponseTime = (stats.AverageResponseTime*float64(stats.MessageCount-1) + responseTime.Seconds()) / float64(stats.MessageCount)

		// Print AI response with color and formatting
		yellow := color.New(color.FgYellow).SprintFunc()
		fmt.Printf("\n%s %s\n", yellow("AI >"), response)
		
		// Show response time for quick feedback
		if responseTime.Seconds() > 2.0 {
			dim := color.New(color.FgHiBlack).SprintFunc()
			fmt.Printf("%s (%.1fs)\n", dim("    "), responseTime.Seconds())
		}
	}
} 