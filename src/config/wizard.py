"""Configuration wizard for TicketPlease first-time setup."""

from pathlib import Path
from typing import Any

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

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
            "Español": "es",
            "English": "en",
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
                Text("🎫 ¡Bienvenido a TicketPlease!", style="bold blue"),
                title="[bold]Configuración Inicial[/bold]",
                border_style="blue",
            )
        )
        console.print()

        console.print(
            "Parece que es la primera vez que usas TicketPlease o tu configuración está vacía.\n"
            "Te guiaremos a través de la configuración inicial.\n"
        )

        # Collect configuration
        config_data = self._collect_llm_config()
        config_data.update(self._collect_preferences())

        # Save configuration
        self.config.save(config_data)

        console.print()
        console.print(
            Panel.fit(
                "✅ ¡Configuración completada exitosamente!",
                title="[bold green]Listo[/bold green]",
                border_style="green",
            )
        )
        console.print()

        return config_data

    def _collect_llm_config(self) -> dict[str, Any]:
        """Collect LLM configuration from user."""
        console.print("[bold]Configuración del Proveedor de IA[/bold]")
        console.print("Estos valores son necesarios para generar las descripciones de tareas.\n")

        # Provider selection
        provider_choice = questionary.select(
            "¿Qué proveedor de IA quieres usar?",
            choices=list(self.providers.keys()),
            default="OpenAI",
        ).ask()

        if not provider_choice:
            raise KeyboardInterrupt("Configuración cancelada")

        provider = self.providers[provider_choice]

        # API Key
        api_key = questionary.password(
            f"Introduce tu API Key para {provider_choice}:",
            validate=lambda x: bool(x.strip()) or "La API Key no puede estar vacía",
        ).ask()

        if not api_key:
            raise KeyboardInterrupt("Configuración cancelada")

        # Model selection
        available_models = self.models[provider]
        model = questionary.select(
            "¿Qué modelo quieres usar?", choices=available_models, default=available_models[0]
        ).ask()

        if not model:
            raise KeyboardInterrupt("Configuración cancelada")

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
        console.print("\n[bold]Preferencias Generales[/bold]")
        console.print("Estas preferencias se pueden modificar posteriormente para cada tarea.\n")

        # Output language
        language_choice = questionary.select(
            "¿En qué idioma quieres generar las descripciones?",
            choices=list(self.languages.keys()),
            default="Español",
        ).ask()

        if not language_choice:
            raise KeyboardInterrupt("Configuración cancelada")

        language = self.languages[language_choice]

        # Platform
        platform_choice = questionary.select(
            "¿Cuál es tu plataforma principal?",
            choices=list(self.platforms.keys()),
            default="GitHub",
        ).ask()

        if not platform_choice:
            raise KeyboardInterrupt("Configuración cancelada")

        platform = self.platforms[platform_choice]

        # Optional file paths
        console.print("\n[bold]Archivos Opcionales[/bold]")
        console.print("Puedes especificar archivos con plantillas por defecto (opcional):\n")

        # Acceptance criteria path
        ac_path = questionary.path(
            "Ruta al archivo de Criterios de Aceptación (opcional):",
            default="",
            validate=lambda x: self._validate_optional_path(x),
        ).ask()

        if ac_path is None:
            raise KeyboardInterrupt("Configuración cancelada")

        # Definition of done path
        dod_path = questionary.path(
            "Ruta al archivo de Definition of Done (opcional):",
            default="",
            validate=lambda x: self._validate_optional_path(x),
        ).ask()

        if dod_path is None:
            raise KeyboardInterrupt("Configuración cancelada")

        return {
            "preferences": {
                "default_output_language": language,
                "default_platform": platform,
                "default_ac_path": ac_path.strip() if ac_path else "",
                "default_dod_path": dod_path.strip() if dod_path else "",
            }
        }

    def _validate_optional_path(self, path: str) -> bool | str:
        """Validate optional file path."""
        if not path or not path.strip():
            return True  # Empty path is valid (optional)

        path_obj = Path(path.strip())
        if not path_obj.exists():
            return f"El archivo '{path}' no existe"

        if not path_obj.is_file():
            return f"'{path}' no es un archivo válido"

        return True
