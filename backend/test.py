import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
  }),
)

# Check if the request was successful
if response.status_code == 200:
    print(response.json()) # This will parse the JSON response and print it
else:
    print(f"Error: {response.status_code}")
    print(response.text) # Print the raw text for error debugging