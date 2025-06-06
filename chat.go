package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

// ChatStats tracks conversation statistics
type ChatStats struct {
	MessageCount        int
	TotalTokens        int
	AverageResponseTime float64
}

// Message represents a chat message
type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

// ChatClient handles communication with the OpenRouter API
type ChatClient struct {
	config     *Config
	httpClient *http.Client
	messages   []Message
}

// NewChatClient creates a new chat client
func NewChatClient(config *Config) *ChatClient {
	return &ChatClient{
		config:     config,
		httpClient: &http.Client{},
		messages: []Message{
			{
				Role:    "system",
				Content: "You are a helpful AI assistant.",
			},
		},
	}
}

// GetResponse gets a response from the AI model
func (c *ChatClient) GetResponse(input string) (string, error) {
	// Add user message to history
	c.messages = append(c.messages, Message{
		Role:    "user",
		Content: input,
	})

	// Prepare request body
	requestBody := map[string]interface{}{
		"model": c.config.Model,
		"messages": c.messages,
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return "", fmt.Errorf("error marshaling request: %v", err)
	}

	// Create request
	req, err := http.NewRequest("POST", "https://openrouter.ai/api/v1/chat/completions", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("error creating request: %v", err)
	}

	// Set headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.config.OpenRouterAPIKey)
	req.Header.Set("HTTP-Referer", c.config.AppURL)
	req.Header.Set("X-Title", c.config.AppName)

	// Send request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("error sending request: %v", err)
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response: %v", err)
	}

	// Check for error response
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("API error (status %d): %s", resp.StatusCode, string(body))
	}

	// Parse response
	var response struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.Unmarshal(body, &response); err != nil {
		return "", fmt.Errorf("error parsing response: %v", err)
	}

	if len(response.Choices) == 0 {
		return "", fmt.Errorf("no response from AI model")
	}

	// Get the response content
	content := response.Choices[0].Message.Content

	// Add assistant message to history
	c.messages = append(c.messages, Message{
		Role:    "assistant",
		Content: content,
	})

	// Keep only the last 10 messages to manage context length
	if len(c.messages) > 11 { // 1 system message + 10 conversation messages
		c.messages = append(c.messages[:1], c.messages[len(c.messages)-10:]...)
	}

	return content, nil
}

// StreamMessage streams a message from the AI model
func (c *ChatClient) StreamMessage(messages []Message, callback func(string)) error {
	// Prepare request body
	requestBody := map[string]interface{}{
		"model": c.config.Model,
		"messages": messages,
		"stream": true,
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return fmt.Errorf("error marshaling request: %v", err)
	}

	// Create request
	req, err := http.NewRequest("POST", "https://openrouter.ai/api/v1/chat/completions", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	// Set headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.config.OpenRouterAPIKey)
	req.Header.Set("HTTP-Referer", c.config.AppURL)
	req.Header.Set("X-Title", c.config.AppName)

	// Send request
	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("error sending request: %v", err)
	}
	defer resp.Body.Close()

	// Check for error response
	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("API error (status %d): %s", resp.StatusCode, string(body))
	}

	// Read response stream
	reader := bufio.NewReader(resp.Body)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			return fmt.Errorf("error reading stream: %v", err)
		}

		// Skip empty lines
		if strings.TrimSpace(line) == "" {
			continue
		}

		// Remove "data: " prefix
		line = strings.TrimPrefix(line, "data: ")

		// Check for end of stream
		if strings.TrimSpace(line) == "[DONE]" {
			break
		}

		// Parse JSON response
		var response struct {
			Choices []struct {
				Delta struct {
					Content string `json:"content"`
				} `json:"delta"`
			} `json:"choices"`
		}

		if err := json.Unmarshal([]byte(line), &response); err != nil {
			return fmt.Errorf("error parsing stream response: %v", err)
		}

		if len(response.Choices) > 0 {
			content := response.Choices[0].Delta.Content
			if content != "" {
				callback(content)
			}
		}
	}

	return nil
} 