#!/usr/bin/env python3

import click
from rich.console import Console
from rich.panel import Panel

from .config import Config
from .chat import OneShot, InteractiveChat
from .providers import get_provider_names

console = Console()


@click.group()
@click.version_option()
def main():
    """lil-llm: A CLI tool for interacting with large language models via BYOK."""
    pass


@main.command()
@click.option(
    "--provider",
    "-p",
    type=click.Choice(get_provider_names()),
    required=True,
    help="LLM provider to use",
)
@click.option(
    "--model", "-m", help="Specific model to use (optional, uses provider default)"
)
@click.option(
    "--api-key",
    "-k",
    help="API key (can also use environment variables or config file)",
)
@click.argument("prompt")
def chat(provider: str, model: str, api_key: str, prompt: str):
    """Send a one-shot prompt to the specified LLM provider."""
    try:
        config = Config(provider=provider, model=model, api_key=api_key)
        one_shot = OneShot(config)
        response = one_shot.send(prompt)

        console.print(
            Panel(
                response,
                title=f"Response from {provider.upper()}"
                + (f" ({model})" if model else ""),
                border_style="green",
            )
        )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
@click.option(
    "--provider",
    "-p",
    type=click.Choice(get_provider_names()),
    required=True,
    help="LLM provider to use",
)
@click.option(
    "--model", "-m", help="Specific model to use (optional, uses provider default)"
)
@click.option(
    "--api-key",
    "-k",
    help="API key (can also use environment variables or config file)",
)
def interactive(provider: str, model: str, api_key: str):
    """Start an interactive chat session with the specified LLM provider."""
    try:
        config = Config(provider=provider, model=model, api_key=api_key)
        interactive_chat = InteractiveChat(config)
        interactive_chat.start()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
