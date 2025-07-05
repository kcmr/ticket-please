"""Tests for the main ticketplease orchestrator module."""

from unittest.mock import patch

from ticketplease.main import run_interactive_flow


def test_run_interactive_flow_with_existing_config():
    """Test that run_interactive_flow executes without errors when config exists."""
    with (
        patch("ticketplease.main.console") as mock_console,
        patch("ticketplease.main.Config") as mock_config_class,
    ):
        # Mock config to simulate existing valid configuration
        mock_config = mock_config_class.return_value
        mock_config.is_first_run.return_value = False
        mock_config.is_configured.return_value = True

        run_interactive_flow()

        # Verify that console.print was called
        assert mock_console.print.call_count >= 1

        # Verify the welcome message is printed
        calls = mock_console.print.call_args_list
        welcome_call = calls[-3]  # Welcome message should be near the end
        assert "🎫 Welcome to TicketPlease!" in str(welcome_call)


def test_run_interactive_flow_first_run():
    """Test run_interactive_flow on first run (triggers wizard)."""
    with (
        patch("ticketplease.main.console") as mock_console,
        patch("ticketplease.main.Config") as mock_config_class,
        patch("ticketplease.main.ConfigWizard") as mock_wizard_class,
    ):
        # Mock config to simulate first run
        mock_config = mock_config_class.return_value
        mock_config.is_first_run.return_value = True
        mock_config.is_configured.return_value = False

        # Mock wizard
        mock_wizard = mock_wizard_class.return_value
        mock_wizard.run.return_value = {"api_keys": {"provider": "openai"}}

        run_interactive_flow()

        # Verify wizard was instantiated and run
        mock_wizard_class.assert_called_once()
        mock_wizard.run.assert_called_once()

        # Verify welcome message is eventually printed
        calls = mock_console.print.call_args_list
        welcome_messages = [call for call in calls if "🎫 Welcome to TicketPlease!" in str(call)]
        assert len(welcome_messages) >= 1


def test_run_interactive_flow_wizard_cancelled():
    """Test run_interactive_flow when wizard is cancelled."""
    with (
        patch("ticketplease.main.console") as mock_console,
        patch("ticketplease.main.Config") as mock_config_class,
        patch("ticketplease.main.ConfigWizard") as mock_wizard_class,
    ):
        # Mock config to simulate first run
        mock_config = mock_config_class.return_value
        mock_config.is_first_run.return_value = True
        mock_config.is_configured.return_value = False

        # Mock wizard to raise KeyboardInterrupt
        mock_wizard = mock_wizard_class.return_value
        mock_wizard.run.side_effect = KeyboardInterrupt("User cancelled")

        run_interactive_flow()

        # Verify cancellation message was printed
        calls = mock_console.print.call_args_list
        cancel_messages = [call for call in calls if "cancelled" in str(call)]
        assert len(cancel_messages) >= 1
