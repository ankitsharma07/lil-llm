import sys
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text

from .config import Config
from .providers import PROVIDERS


console = Console()


class OneShot:
    """One-shot chat interface."""

    def __init__(self, config: Config):
        self.config = config
        self.provider = self._get_provider()

    def _get_provider(self):
        """Get the appropriate provider instance."""
        provider_class = PROVIDERS.get(self.config.provider.lower())
        if not provider_class:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

        return provider_class(self.config.api_key, self.config.effective_model)

    def send(self, prompt: str) -> str:
        """Send a prompt and get response."""
        return self.provider.send_message(prompt)


class InteractiveChat:
    """Interactive chat interface."""

    def __init__(self, config: Config):
        self.config = config
        self.provider = self._get_provider()
        self.conversation: List[Dict[str, str]] = []

    def _get_provider(self):
        """Get the appropriate provider instance."""
        provider_class = PROVIDERS.get(self.config.provider.lower())
        if not provider_class:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

        return provider_class(self.config.api_key, self.config.effective_model)

    def start(self):
        """Start interactive chat session."""
        model_info = f" ({self.config.effective_model})" if self.config.model else ""
        console.print(
            Panel(
                f"Starting interactive chat with [bold]{self.config.provider.upper()}[/bold]{model_info}\n"
                f"Type 'quit', 'exit', or press Ctrl+C to end the session.\n"
                f"Type '/clear' to clear conversation history.",
                title="Interactive Chat",
                border_style="blue",
            )
        )

        try:
            while True:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")

                if user_input.lower() in ["quit", "exit"]:
                    break

                if user_input.lower() == "/clear":
                    self.conversation = []
                    console.print("[yellow]Conversation history cleared.[/yellow]")
                    continue

                # Add user message to conversation
                self.conversation.append({"role": "user", "content": user_input})

                # Get response with streaming
                console.print(
                    f"\n[bold green]{self.config.provider.upper()}[/bold green]:"
                )
                response_text = ""

                with Live(Text(""), refresh_per_second=10) as live:
                    for chunk in self.provider.stream_response(self.conversation):
                        response_text += chunk
                        live.update(Text(response_text))

                # Add assistant response to conversation
                self.conversation.append(
                    {"role": "assistant", "content": response_text}
                )

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat session ended.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
