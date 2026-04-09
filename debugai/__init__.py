from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.nvidia import NvidiaProvider

# Auto-detection order: first available key wins
PROVIDERS = [
    OpenAIProvider(),
    AnthropicProvider(),
    NvidiaProvider(),
]

__all__ = ["OpenAIProvider", "AnthropicProvider", "NvidiaProvider", "PROVIDERS"]
