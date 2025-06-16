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