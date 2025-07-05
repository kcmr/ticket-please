"""Main orchestrator for TicketPlease application."""

from rich.console import Console
from rich.text import Text

from config.service import Config
from config.wizard import ConfigWizard

console = Console()


def run_interactive_flow() -> None:
    """Run the interactive task generation flow."""
    config = Config()

    # Check if configuration is needed
    if config.is_first_run() or not config.is_configured():
        try:
            wizard = ConfigWizard()
            wizard.run()
        except KeyboardInterrupt:
            console.print("\n❌ Configuración cancelada. Saliendo...")
            return
        except Exception as e:
            console.print(f"\n❌ Error en la configuración: {e}")
            return

    console.print(Text("🎫 Welcome to TicketPlease!", style="bold blue"))
    console.print("Starting interactive task generation...")
    console.print("This feature is coming soon!")
