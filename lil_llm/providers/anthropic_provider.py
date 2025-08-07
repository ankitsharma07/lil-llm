from typing import List, Dict
from anthropic import Anthropic
from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider."""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = Anthropic(api_key=api_key)

    def send_message(self, prompt: str) -> str:
        """Send a single message and get response."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def send_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Send a conversation and get response."""
        response = self.client.messages.create(
            model=self.model, max_tokens=4000, messages=messages
        )
        return response.content[0].text

    def stream_response(self, messages: List[Dict[str, str]]):
        """Stream response tokens."""
        with self.client.messages.stream(
            model=self.model, max_tokens=4000, messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text
