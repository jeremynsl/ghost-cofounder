#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

def main():
    # Accept prompt from stdin if piped, else from argv
    prompt = sys.stdin.read().strip() if not sys.stdin.isatty() else " ".join(sys.argv[1:])
    if not prompt:
        print("Usage: python3 ghost_cofounder.py 'your question here' or echo 'your question' | python3 ghost_cofounder.py")
        sys.exit(1)

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    # Prepare request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Load model and system prompt from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Create it or copy config.example.json")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: config.json invalid JSON: {e}")
        sys.exit(1)
    model = config.get('model')
    system_prompt = config.get('system_prompt')

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    # Make request
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            headers=headers
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # Extract and print response
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(content)
        else:
            print("Error: No response received from API")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error making API request: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
