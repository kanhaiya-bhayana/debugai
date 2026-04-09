import os
from .base import AIProvider


class OpenAIProvider(AIProvider):

    MODEL = "gpt-4o-mini"

    def name(self) -> str:
        return "OpenAI"

    def is_available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    def analyze(self, prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": "You are an expert debugging assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )

        return completion.choices[0].message.content
