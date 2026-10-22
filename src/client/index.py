from google.genai import Client
from google.genai._gaos.utils.eventstreaming import Stream
from google.genai.interactions import Interaction, InteractionSSEEvent
from src.config.env import env_variables
from src.tools.functions_def import run_tool
from src.tools.functions_list import TOOLS
from typing import Any


INSTRUCTIONS = (
    "You are concise and always reply in French. Use remember to retain a fact, "
    "recall for memory, and web_search for current "
    "online information. Cite source URLs returned by web_search."
    "Never invent tool results."
)


class GoogleAIClient:
    def __init__(self) -> None:
        if not env_variables.google_api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is missing. Create .env from .env.example."
            )

        self.client = Client(api_key=env_variables.google_api_key)

    def response(
        self,
        user_input: Any,
        previous_interaction_id: str | None = None,
        model: str = "gemini-flash-latest",
    ) -> Interaction | Stream[InteractionSSEEvent]:
        kwargs: dict[str, Any] = {
            "model": model,
            "input": user_input,
            "tools": TOOLS,
            "system_instruction": INSTRUCTIONS,
        }
        if previous_interaction_id:
            kwargs["previous_interaction_id"] = previous_interaction_id

        return self.client.interactions.create(**kwargs)

    def ask(self, message: str, user_id: str = "guest"):
        current_input: Any = message
        previous_interaction_id: str | None = None

        while True:
            interaction = self.response(
                user_input=current_input,
                previous_interaction_id=previous_interaction_id,
            )

            if isinstance(interaction, Interaction):
                function_calls = [
                    step
                    for step in (interaction.steps or [])
                    if step.type == "function_call"
                ]

                if not function_calls:
                    return interaction.output_text

                previous_interaction_id = interaction.id

                function_results = []
                for fn in function_calls:
                    result = run_tool(fn.name, fn.arguments, user_id=user_id)
                    print(f"\tCalled {fn.name}({fn.arguments}) → {result}")

                    function_results.append(
                        {
                            "type": "function_result",
                            "name": fn.name,
                            "call_id": fn.id,
                            "result": result,
                        }
                    )

                current_input = function_results
