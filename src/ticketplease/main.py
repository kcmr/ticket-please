"""Main orchestrator for TicketPlease application."""

from rich.console import Console

from config.service import Config
from config.wizard import ConfigWizard

from .generator import TaskGenerator

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

        # After successful initial setup, start task generation
        if not is_update:
            run_task_generation()
        return

    # If this is not an update, start task generation
    if not is_update:
        run_task_generation()
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


def run_task_generation() -> None:
    """Run the task generation flow."""
    config = Config()
    generator = TaskGenerator(config)
    generator.generate_task()
