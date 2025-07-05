"""Main orchestrator for TicketPlease application."""

from rich.console import Console

from config.service import Config
from config.wizard import ConfigWizard

console = Console()


def run_wizard() -> None:
    """Run the configuration wizard."""
    config = Config()

    # Check if configuration is needed
    if config.is_first_run() or not config.is_configured():
        try:
            wizard = ConfigWizard()
            wizard.run()
        except KeyboardInterrupt:
            console.print("\n❌ Configuration cancelled. Exiting...")
            return
        except Exception as e:
            console.print(f"\n❌ Configuration error: {e}")
            return


def run_config_update() -> None:
    """Run the configuration update flow."""
    config = Config()

    # Check if configuration exists
    if config.is_first_run():
        console.print("[yellow]No configuration found. Launching initial setup wizard...[/yellow]")
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

    try:
        wizard = ConfigWizard()
        wizard.run_update()
    except KeyboardInterrupt:
        console.print("\n❌ Configuration update cancelled.")
        return
    except Exception as e:
        console.print(f"\n❌ Configuration update error: {e}")
        return
