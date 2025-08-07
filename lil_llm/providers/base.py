from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def send_message(self, prompt: str) -> str:
        """Send a single message and get response."""
        pass

    @abstractmethod
    def send_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Send a conversation and get response."""
        pass

    @abstractmethod
    def stream_response(self, prompt: str):
        """Stream response tokens."""
        pass
