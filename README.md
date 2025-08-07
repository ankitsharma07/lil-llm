# lil-llm

A CLI tool for interacting with large language models via BYOK (Bring Your Own Key).

## Features

- Support for multiple LLM providers (OpenAI, Anthropic, Google)
- One-shot chat mode for quick queries
- Interactive thread-style chat sessions
- Flexible API key management (environment variables, config files, or command-line)
- Rich terminal interface with syntax highlighting

## Installation

```bash
# Install in development mode
pip install -e .

# Or install dependencies manually
pip install click openai anthropic google-generativeai rich python-dotenv pydantic
