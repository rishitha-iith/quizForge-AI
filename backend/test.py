import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        # Optional headers for site metadata on OpenRouter.ai:
        # "HTTP-Referer": "https://quizforge.ai",
        # "X-Title": "QuizForge AI",
    },
    json={  # ✅ You can use `json=` directly instead of `data=json.dumps(...)`
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    }
)

# ✅ Handle response
if response.status_code == 200:
    result = response.json()
    print("Response from model:")
    print(result["choices"][0]["message"]["content"])
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
