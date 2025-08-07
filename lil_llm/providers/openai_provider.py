from typing import List, Dict
from openai import OpenAI
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)

    def send_message(self, prompt: str) -> str:
        """Send a single message and get response."""
        response = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def send_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Send a conversation and get response."""
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content

    def stream_response(self, messages: List[Dict[str, str]]):
        """Stream response tokens."""
        stream = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
