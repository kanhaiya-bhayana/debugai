import os
from .base import AIProvider


class AnthropicProvider(AIProvider):

    MODEL = "claude-haiku-4-5-20251001"

    def name(self) -> str:
        return "Anthropic"

    def is_available(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    def analyze(self, prompt: str) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model=self.MODEL,
            max_tokens=2000,
            system="You are an expert debugging assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
