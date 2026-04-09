import json
import re
from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name, e.g. 'OpenAI'."""
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the required env var / credentials are present."""
        raise NotImplementedError

    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """Send prompt to the model and return raw text response."""
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    #  Shared helpers — all providers use these                           #
    # ------------------------------------------------------------------ #

    def parse_response(self, text: str) -> dict:
        """
        Parse the model's response into a structured dict.
        Tries strict JSON first, then extracts a JSON block, then falls back
        to returning the raw text as root_cause.
        """
        try:
            return json.loads(text)
        except Exception:
            pass

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass

        # Last resort: return raw text so the user sees something useful
        return {
            "root_cause": text.strip() or "No response from model.",
            "fix": "",
            "prevention": ""
        }

    def build_prompt(self, log: str) -> str:
        return f"""You are a senior software engineer debugging a production issue.

Return STRICT JSON in this exact format with no other text:

{{
  "root_cause": "...",
  "fix": "...",
  "prevention": "..."
}}

Stack trace:
{log}
"""
