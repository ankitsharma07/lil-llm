from typing import List, Dict
import google.generativeai as genai
from .base import LLMProvider


class GoogleProvider(LLMProvider):
    """Google Generative AI provider."""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def send_message(self, prompt: str) -> str:
        """Send a single message and get response."""
        response = self.client.generate_content(prompt)
        return response.text

    def send_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Send a conversation and get response."""
        # Convert messages to Google's format
        conversation = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            conversation.append({"role": role, "parts": [msg["content"]]})

        chat = self.client.start_chat(history=conversation[:-1])
        response = chat.send_message(conversation[-1]["parts"][0])
        return response.text

    def stream_response(self, messages: List[Dict[str, str]]):
        """Stream response tokens."""
        # Convert messages to Google's format
        conversation = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            conversation.append({"role": role, "parts": [msg["content"]]})

        chat = self.client.start_chat(history=conversation[:-1])
        response = chat.send_message(conversation[-1]["parts"][0], stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text
