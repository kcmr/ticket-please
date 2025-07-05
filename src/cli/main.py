"""Main CLI entry point for TicketPlease."""

import typer
from rich.console import Console

from ticketplease.main import run_config_update, run_wizard

from . import __version__

app = typer.Typer(
    name="tkp",
    help="CLI assistant for generating task descriptions using AI",
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Show the version of TicketPlease."""
    console.print(f"TicketPlease version {__version__}")


@app.command()
def config() -> None:
    """Modify your TicketPlease configuration."""
    run_config_update()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Start the interactive task generation flow."""
    if ctx.invoked_subcommand is None:
        run_wizard()


if __name__ == "__main__":
    app()
