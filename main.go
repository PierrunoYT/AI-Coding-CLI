package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	config, err := LoadConfig()
	if err != nil {
		fmt.Printf("Error loading config: %v\n", err)
		os.Exit(1)
	}

	chatClient := NewChatClient(config)
	messages := []Message{
		{
			Role:    "system",
			Content: "You are a helpful AI assistant.",
		},
	}

	fmt.Println("AI Chat CLI (type 'exit' to quit)")
	fmt.Println("--------------------------------")

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("\nYou: ")
		if !scanner.Scan() {
			break
		}

		input := strings.TrimSpace(scanner.Text())
		if input == "exit" {
			break
		}

		messages = append(messages, Message{
			Role:    "user",
			Content: input,
		})

		fmt.Print("\nAI: ")
		var responseBuilder strings.Builder
		err := chatClient.StreamMessage(messages, func(chunk string) {
			fmt.Print(chunk)
			responseBuilder.WriteString(chunk)
		})
		fmt.Println() // New line after response

		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}

		messages = append(messages, Message{
			Role:    "assistant",
			Content: responseBuilder.String(),
		})
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading input: %v\n", err)
	}
} 