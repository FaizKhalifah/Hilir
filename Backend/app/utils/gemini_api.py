import requests

class GeminiAPI:
    @staticmethod
    def get_exercises_for_issues(issues):
        try:
            response = requests.post(
                'https://geminiapi.com/exercises',  # Replace with real Gemini API URL
                json={"mental_health_issues": issues},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json().get("exercises"), None
        except requests.exceptions.RequestException as e:
            return None, str(e)
