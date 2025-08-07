import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file if it exists
load_dotenv()


class Config(BaseModel):
    """Configuration for LLM interactions."""

    provider: str = Field(..., description="LLM provider name")
    model: Optional[str] = Field(None, description="Specific model to use")
    api_key: Optional[str] = Field(None, description="API key for the provider")

    def __post_init__(self):
        """Post-initialization to resolve API key."""
        if not self.api_key:
            self.api_key = self._get_api_key()

    def model_post_init(self, __context) -> None:
        """Post-initialization hook for Pydantic v2."""
        if not self.api_key:
            self.api_key = self._get_api_key()

    def _get_api_key(self) -> str:
        """Get API key from various sources."""
        # Try provider-specific environment variables
        env_vars = {
            "openai": ["OPENAI_API_KEY", "OPENAI_TOKEN"],
            "anthropic": ["ANTHROPIC_API_KEY", "CLAUDE_API_KEY"],
            "google": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
            "cohere": ["COHERE_API_KEY"],
        }

        if self.provider.lower() in env_vars:
            for env_var in env_vars[self.provider.lower()]:
                key = os.getenv(env_var)
                if key:
                    return key

        # Try generic environment variable
        generic_key = os.getenv("LLM_API_KEY")
        if generic_key:
            return generic_key

        # Try reading from config file
        config_file = Path.home() / ".config" / "lil-llm" / "config.env"
        if config_file.exists():
            load_dotenv(config_file)
            for env_var in env_vars.get(self.provider.lower(), []):
                key = os.getenv(env_var)
                if key:
                    return key

        raise ValueError(
            f"No API key found for {self.provider}. "
            f"Please provide it via --api-key option, environment variable, or config file."
        )

    @property
    def default_model(self) -> str:
        """Get default model for the provider."""
        defaults = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-sonnet-20240229",
            "google": "gemini-pro",
            "cohere": "command",
        }
        return defaults.get(self.provider.lower(), "default")

    @property
    def effective_model(self) -> str:
        """Get the model to use (provided or default)."""
        return self.model or self.default_model
