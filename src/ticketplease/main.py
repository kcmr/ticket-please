"""Main orchestrator for TicketPlease application."""

from rich.console import Console

from config.service import Config
from config.wizard import ConfigWizard

console = Console()


def run_config(is_update: bool = False) -> None:
    """Unified method to handle both initial setup and configuration updates."""
    config = Config()

    # Check if configuration exists
    if config.is_first_run():
        if is_update:
            console.print(
                "[yellow]No configuration found. Launching initial setup wizard...[/yellow]"
            )
            console.print()
        try:
            wizard = ConfigWizard()
            wizard.run()
        except KeyboardInterrupt:
            console.print("\n❌ Configuration cancelled.")
            return
        except Exception as e:
            console.print(f"\n❌ Configuration error: {e}")
            return
        return

    # If this is not an update, we don't need to do anything
    if not is_update:
        return

    try:
        wizard = ConfigWizard()
        wizard.run_update()
    except KeyboardInterrupt:
        console.print("\n❌ Configuration update cancelled.")
        return
    except Exception as e:
        console.print(f"\n❌ Configuration update error: {e}")
        return
