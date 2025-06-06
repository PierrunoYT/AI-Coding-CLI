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

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ChatRequest struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
	Stream   bool      `json:"stream,omitempty"`
}

type ChatResponse struct {
	ID      string `json:"id"`
	Choices []struct {
		Message      Message `json:"message"`
		FinishReason string  `json:"finish_reason"`
		Delta        *Message `json:"delta,omitempty"`
	} `json:"choices"`
	Usage struct {
		PromptTokens     int `json:"prompt_tokens"`
		CompletionTokens int `json:"completion_tokens"`
		TotalTokens      int `json:"total_tokens"`
	} `json:"usage"`
}

type ChatClient struct {
	config *Config
	client *http.Client
}

func NewChatClient(config *Config) *ChatClient {
	return &ChatClient{
		config: config,
		client: &http.Client{},
	}
}

// StreamMessage sends a message and streams the response
func (c *ChatClient) StreamMessage(messages []Message, callback func(string)) error {
	reqBody := ChatRequest{
		Model:    c.config.Model,
		Messages: messages,
		Stream:   true,
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return fmt.Errorf("error marshaling request: %v", err)
	}

	req, err := http.NewRequest("POST", "https://openrouter.ai/api/v1/chat/completions", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	// Set required headers according to OpenRouter documentation
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.config.OpenRouterAPIKey)
	req.Header.Set("HTTP-Referer", c.config.AppURL)    // Required for rankings
	req.Header.Set("X-Title", c.config.AppName)        // Required for rankings
	req.Header.Set("OpenAI-Organization", "org-123")   // Optional: for OpenAI models

	resp, err := c.client.Do(req)
	if err != nil {
		return fmt.Errorf("error making request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("API error (status %d): %s", resp.StatusCode, string(body))
	}

	reader := bufio.NewReader(resp.Body)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			return fmt.Errorf("error reading stream: %v", err)
		}

		line = strings.TrimSpace(line)
		if !strings.HasPrefix(line, "data: ") {
			continue
		}

		data := strings.TrimPrefix(line, "data: ")
		if data == "[DONE]" {
			break
		}

		var chatResp ChatResponse
		if err := json.Unmarshal([]byte(data), &chatResp); err != nil {
			return fmt.Errorf("error unmarshaling stream data: %v", err)
		}

		if len(chatResp.Choices) > 0 && chatResp.Choices[0].Delta != nil {
			content := chatResp.Choices[0].Delta.Content
			if content != "" {
				callback(content)
			}
		}
	}

	return nil
}

// SendMessage sends a message and returns the complete response
func (c *ChatClient) SendMessage(messages []Message) (string, error) {
	var fullResponse strings.Builder
	err := c.StreamMessage(messages, func(chunk string) {
		fullResponse.WriteString(chunk)
	})
	if err != nil {
		return "", err
	}
	return fullResponse.String(), nil
} 