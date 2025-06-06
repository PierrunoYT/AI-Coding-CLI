#!/usr/bin/env python3
"""
Simple script to test OpenRouter API connection
"""
import os
import requests

def test_openrouter_connection():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("Please set it with: export OPENROUTER_API_KEY=your_key_here")
        return False
    
    print("✅ API key found and loaded")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Test models endpoint
    try:
        print("🔄 Testing connection to OpenRouter...")
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Connection successful! Found {len(data.get('data', []))} models")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if response.status_code == 401:
            print("   → Authentication failed. Check your API key.")
        elif response.status_code == 403:
            print("   → Access forbidden. Your API key may not have the required permissions.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_openrouter_connection() 