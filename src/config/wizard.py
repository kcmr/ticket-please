"""Configuration wizard for TicketPlease first-time setup."""

from pathlib import Path
from typing import Any

import litellm
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
        self.models = self._get_supported_models()
        self.languages = {
            "English": "en",
            "Español": "es",
        }
        self.platforms = {
            "GitHub": "github",
            "Jira": "jira",
        }

    def _get_supported_models(self) -> dict[str, list[str]]:
        """Return a dictionary of provider -> list of supported models using litellm provider-specific lists."""
        models_by_provider = {
            "openai": self._get_openai_models(),
            "anthropic": self._get_anthropic_models(),
            "gemini": self._get_gemini_models(),
            "openrouter": self._get_openrouter_models(),
        }

        # Add custom model option to each provider
        for provider in models_by_provider:
            models_by_provider[provider].append("🔧 Specify custom model")

        return models_by_provider

    def _get_openai_models(self) -> list[str]:
        """Get OpenAI models from litellm."""
        # Use litellm's OpenAI-specific model list
        openai_models = litellm.open_ai_chat_completion_models

        # Filter out fine-tuned and special models
        filtered_models = [
            m
            for m in openai_models
            if not m.startswith("ft:") and not m.startswith("omni-") and "gpt" in m.lower()
        ]

        # Preferred order - exact matches first, then partial matches
        preferred_exact = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        sorted_models = []

        # Add exact matches first
        for preferred in preferred_exact:
            if preferred in filtered_models:
                sorted_models.append(preferred)

        # Add partial matches (versioned models)
        for preferred in preferred_exact:
            matching = [
                m
                for m in filtered_models
                if m.startswith(preferred + "-") and m not in sorted_models
            ]
            matching.sort(reverse=True)  # Latest versions first
            sorted_models.extend(matching)

        # Add o1 models
        o1_models = [m for m in filtered_models if m.startswith("o1-")]
        o1_models.sort(reverse=True)
        sorted_models.extend(o1_models)

        # Add remaining models
        remaining = [m for m in filtered_models if m not in sorted_models]
        sorted_models.extend(sorted(remaining))

        return sorted_models[:15]  # Limit to top 15

    def _get_anthropic_models(self) -> list[str]:
        """Get Anthropic models from litellm."""
        # Use litellm's Anthropic-specific model list
        anthropic_models = litellm.anthropic_models

        # Preferred order
        preferred_order = [
            "claude-3-5-sonnet",
            "claude-3-5-haiku",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
        ]
        sorted_models = []

        for preferred in preferred_order:
            matching = [m for m in anthropic_models if preferred in m]
            matching.sort(reverse=True)  # Latest versions first
            sorted_models.extend(matching)

        # Add remaining models
        remaining = [m for m in anthropic_models if not any(p in m for p in preferred_order)]
        sorted_models.extend(sorted(remaining))

        return sorted_models[:15]  # Limit to top 15

    def _get_gemini_models(self) -> list[str]:
        """Get Gemini models from litellm."""
        # Use litellm's Gemini-specific model list
        gemini_models = litellm.gemini_models

        # Preferred order
        preferred_order = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-2.0"]
        sorted_models = []

        for preferred in preferred_order:
            matching = [m for m in gemini_models if preferred in m]
            matching.sort(reverse=True)  # Latest versions first
            sorted_models.extend(matching)

        # Add remaining models
        remaining = [m for m in gemini_models if not any(p in m for p in preferred_order)]
        sorted_models.extend(sorted(remaining))

        return sorted_models[:15]  # Limit to top 15

    def _get_openrouter_models(self) -> list[str]:
        """Get OpenRouter models from litellm."""
        # Use litellm's OpenRouter-specific model list
        openrouter_models = litellm.openrouter_models

        # Preferred models
        preferred_models = [
            "anthropic/claude-3-5-sonnet",
            "anthropic/claude-3-5-haiku",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "google/gemini-pro-1.5",
            "meta-llama/llama-3.1-8b-instruct",
        ]

        sorted_models = []
        for preferred in preferred_models:
            if preferred in openrouter_models:
                sorted_models.append(preferred)

        # Add remaining models from major providers
        remaining = [
            m
            for m in openrouter_models
            if m not in sorted_models
            and any(
                provider in m.lower()
                for provider in ["anthropic", "openai", "google", "meta-llama"]
            )
        ]
        sorted_models.extend(sorted(remaining))

        return sorted_models[:15]  # Limit to top 15

    def run(self) -> bool:
        """Run the configuration wizard."""
        try:
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

            return True

        except KeyboardInterrupt:
            console.print("\n[yellow]Configuration cancelled.[/yellow]")
            return False

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
        model_choice = questionary.select(
            "Which model would you like to use?",
            choices=available_models,
            default=available_models[0] if available_models else "🔧 Specify custom model",
        ).ask()

        if not model_choice:
            raise KeyboardInterrupt("Configuration cancelled")

        # Handle custom model specification
        if model_choice == "🔧 Specify custom model":
            console.print()
            console.print("[bold yellow]Custom Model Specification[/bold yellow]")
            console.print("Enter the exact model name as supported by your provider.")
            console.print("Examples:")
            console.print("  - For OpenAI: gpt-4o-2024-11-20, gpt-4o-mini-2024-07-18")
            console.print(
                "  - For Anthropic: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022"
            )
            console.print("  - For Gemini: gemini-1.5-pro-latest, gemini-2.0-flash-exp")
            console.print("  - For OpenRouter: anthropic/claude-3.5-sonnet, openai/gpt-4o")
            console.print()

            model = questionary.text(
                "Enter custom model name:",
                validate=lambda x: bool(x.strip()) or "Model name cannot be empty",
            ).ask()

            if not model:
                raise KeyboardInterrupt("Configuration cancelled")
        else:
            model = model_choice

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

        return {
            "preferences": {
                "default_output_language": language,
                "default_platform": platform,
                "default_ac_path": expand_file_path(ac_path) if ac_path else "",
                "default_dod_path": expand_file_path(dod_path) if dod_path else "",
            }
        }

    def _validate_optional_path(self, path: str) -> bool | str:
        """Validate optional file path."""
        if not path or not path.strip():
            return True  # Empty path is valid (optional)

        expanded_path = expand_file_path(path)
        file_path = Path(expanded_path)

        if not file_path.exists():
            return f"File does not exist: {expanded_path}"

        if not file_path.is_file():
            return f"Path is not a file: {expanded_path}"

        return True
