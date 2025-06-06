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
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printModelInfo() {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("Model Information:"))
	fmt.Printf("%s %s\n", yellow("• Current Model:"), green(config.Model))
	fmt.Printf("%s %s\n", yellow("• Context Window:"), green("200,000 tokens"))
	fmt.Printf("%s %s\n", yellow("• Streaming:"), green("Enabled"))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func printStats(stats *ChatStats) {
	cyan := color.New(color.FgCyan).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Printf("\n%s\n", cyan("Conversation Statistics:"))
	fmt.Printf("%s %s\n", yellow("• Messages:"), green(fmt.Sprintf("%d", stats.MessageCount)))
	fmt.Printf("%s %s\n", yellow("• Total Tokens:"), green(fmt.Sprintf("%d", stats.TotalTokens)))
	fmt.Printf("%s %s\n", yellow("• Average Response Time:"), green(fmt.Sprintf("%.2fs", stats.AverageResponseTime)))
	fmt.Printf("%s\n", cyan("────────────────────────────────────────────────────────────"))
}

func main() {
	var err error
	config, err = LoadConfig()
	if err != nil {
		fmt.Printf("Error loading configuration: %v\n", err)
		os.Exit(1)
	}

	chatClient := NewChatClient(config)
	stats := &ChatStats{}

	printWelcome()

	reader := bufio.NewReader(os.Stdin)
	for {
		// Print prompt with color
		cyan := color.New(color.FgCyan).SprintFunc()
		fmt.Printf("\n%s ", cyan("You >"))

		// Read user input
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("Error reading input: %v\n", err)
			continue
		}

		// Trim whitespace and check for exit command
		input = strings.TrimSpace(input)
		if input == "exit" {
			fmt.Println("\nGoodbye!")
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
		case "":
			continue
		}

		// Get response from AI
		startTime := time.Now()
		response, err := chatClient.GetResponse(input)
		if err != nil {
			red := color.New(color.FgRed).SprintFunc()
			fmt.Printf("%s Error: %v\n", red("Error:"), err)
			continue
		}

		// Update statistics
		stats.MessageCount++
		stats.TotalTokens += len(strings.Fields(response))
		stats.AverageResponseTime = (stats.AverageResponseTime*float64(stats.MessageCount-1) + time.Since(startTime).Seconds()) / float64(stats.MessageCount)

		// Print AI response with color
		yellow := color.New(color.FgYellow).SprintFunc()
		fmt.Printf("\n%s %s\n", yellow("AI >"), response)
	}
} 