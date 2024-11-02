
import requests
from app.config import Config

class GeminiAPI:
    @staticmethod
    def get_exercises_for_prompt(prompt):
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 1,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1000,
                "responseMimeType": "text/plain"
            }
        }

        # Retry up to 3 times if needed
        for _ in range(3):
            response = requests.post(
                f"{Config.GEMINI_API_URL}?key={Config.GOOGLE_API_KEY}",
                headers={
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code == 200:
                return response.json(), None
            else:
                error = f"Status code: {response.status_code}, Error: {response.text}"

        return None, error
