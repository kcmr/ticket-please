"""Main CLI entry point for TicketPlease."""

import typer
from rich.console import Console
from rich.text import Text

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
def main() -> None:
    """Start the interactive task generation flow."""
    console.print(Text("🎫 Welcome to TicketPlease!", style="bold blue"))
    console.print("This feature is coming soon!")
    console.print("Use 'tkp --help' to see available commands.")


if __name__ == "__main__":
    app()
