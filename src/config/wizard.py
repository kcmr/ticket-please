"""Configuration wizard for TicketPlease first-time setup."""

from pathlib import Path
from typing import Any

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ticketplease.utils import expand_file_path

from .service import Config

console = Console()


class ConfigWizard:
    """Configuration wizard for first-time setup."""

    def __init__(self) -> None:
        """Initialize the configuration wizard."""
        self.config = Config()
        self.providers = {
            "OpenAI": "openai",
            "Anthropic": "anthropic",
            "Google (Gemini)": "gemini",
            "OpenRouter": "openrouter",
        }
        self.models = {
            "openai": [
                "gpt-4o-mini",
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
            ],
            "anthropic": [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
            ],
            "gemini": [
                "gemini-1.5-pro-latest",
                "gemini-1.5-flash-latest",
                "gemini-1.0-pro-latest",
            ],
            "openrouter": [
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o-mini",
                "google/gemini-pro-1.5",
                "meta-llama/llama-3.1-8b-instruct",
            ],
        }
        self.languages = {
            "English": "en",
            "Español": "es",
        }
        self.platforms = {
            "GitHub": "github",
            "Jira": "jira",
        }

    def run(self) -> dict[str, Any]:
        """Run the configuration wizard."""
        console.print()
        console.print(
            Panel.fit(
                Text("🎫 Welcome to TicketPlease!", style="bold blue"),
                title="[bold]Initial Setup[/bold]",
                border_style="blue",
            )
        )
        console.print()

        console.print(
            "It looks like this is your first time using TicketPlease or your configuration is empty.\n"
            "We'll guide you through the initial setup.\n"
        )

        # Collect configuration
        config_data = self._collect_llm_config()
        config_data.update(self._collect_preferences())

        # Save configuration
        self.config.save(config_data)

        console.print()
        console.print(
            Panel.fit(
                "✅ Configuration completed successfully!",
                title="[bold green]Ready[/bold green]",
                border_style="green",
            )
        )
        console.print()

        return config_data

    def _collect_llm_config(self) -> dict[str, Any]:
        """Collect LLM configuration from user."""
        console.print("[bold]AI Provider Configuration[/bold]")
        console.print("These values are required to generate task descriptions.\n")

        # Provider selection
        provider_choice = questionary.select(
            "Which AI provider would you like to use?",
            choices=list(self.providers.keys()),
            default="OpenAI",
        ).ask()

        if not provider_choice:
            raise KeyboardInterrupt("Configuration cancelled")

        provider = self.providers[provider_choice]

        # API Key
        api_key = questionary.password(
            f"Enter your API Key for {provider_choice}:",
            validate=lambda x: bool(x.strip()) or "API Key cannot be empty",
        ).ask()

        if not api_key:
            raise KeyboardInterrupt("Configuration cancelled")

        # Model selection
        available_models = self.models[provider]
        model = questionary.select(
            "Which model would you like to use?",
            choices=available_models,
            default=available_models[0],
        ).ask()

        if not model:
            raise KeyboardInterrupt("Configuration cancelled")

        return {
            "api_keys": {
                "provider": provider,
                "api_key": api_key.strip(),
            },
            "llm": {
                "model": model,
            },
        }

    def _collect_preferences(self) -> dict[str, Any]:
        """Collect user preferences."""
        console.print("\n[bold]General Preferences[/bold]")
        console.print("These preferences can be modified later for each task.\n")

        # Output language
        language_choice = questionary.select(
            "In which language would you like to generate the descriptions?",
            choices=list(self.languages.keys()),
            default="English",
        ).ask()

        if not language_choice:
            raise KeyboardInterrupt("Configuration cancelled")

        language = self.languages[language_choice]

        # Platform
        platform_choice = questionary.select(
            "What is your primary platform?",
            choices=list(self.platforms.keys()),
            default="GitHub",
        ).ask()

        if not platform_choice:
            raise KeyboardInterrupt("Configuration cancelled")

        platform = self.platforms[platform_choice]

        # Optional file paths
        console.print("\n[bold]Optional Files[/bold]")
        console.print("You can specify files with default templates (optional):\n")

        # Acceptance criteria path
        ac_path = questionary.path(
            "Path to Acceptance Criteria file (optional):",
            default="",
            validate=lambda x: self._validate_optional_path(x),
            only_directories=False,
        ).ask()

        if ac_path is None:
            raise KeyboardInterrupt("Configuration cancelled")

        # Definition of done path
        dod_path = questionary.path(
            "Path to Definition of Done file (optional):",
            default="",
            validate=lambda x: self._validate_optional_path(x),
            only_directories=False,
        ).ask()

        if dod_path is None:
            raise KeyboardInterrupt("Configuration cancelled")

        # Expand paths to absolute paths if provided
        expanded_ac_path = expand_file_path(ac_path) if ac_path else ""
        expanded_dod_path = expand_file_path(dod_path) if dod_path else ""

        return {
            "preferences": {
                "default_output_language": language,
                "default_platform": platform,
                "default_ac_path": expanded_ac_path,
                "default_dod_path": expanded_dod_path,
            }
        }

    def _validate_optional_path(self, path: str) -> bool | str:
        """Validate optional file path."""
        if not path or not path.strip():
            return True  # Empty path is valid (optional)

        # Use the utility function to expand the path
        expanded_path = expand_file_path(path)
        path_obj = Path(expanded_path)

        if not path_obj.exists():
            return f"File '{path}' does not exist"

        if not path_obj.is_file():
            return f"'{path}' is not a valid file"

        return True
