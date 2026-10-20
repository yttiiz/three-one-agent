from google.genai import Client
from src.config.env import env_variables


class GoogleAIClient:
    def __init__(self) -> None:
        self.client = Client(api_key=env_variables.google_api_key)

    def ask(self, user_input: str, model="gemini-3.1-flash-lite-image"):
        response = self.client.models.generate_content(model=model, contents=user_input)
        print(response.text)
