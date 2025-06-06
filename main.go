package main

import (
	"bufio"
	"fmt"
	"os"
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
	if strings.Contains(config.Model, "claude-opus-4") {
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$15/M input, $75/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Complex reasoning, coding"))
	} else if strings.Contains(config.Model, "claude-sonnet-4") {
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$3/M input, $15/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Balanced performance"))
	} else if strings.Contains(config.Model, "claude-3.5-sonnet") {
		fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
		fmt.Printf("%s %s\n", yellow("• Pricing:"), green("$3/M input, $15/M output"))
		fmt.Printf("%s %s\n", yellow("• Best for:"), green("Best value for money"))
	} else {
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