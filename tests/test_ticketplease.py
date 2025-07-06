"""Tests for the main ticketplease orchestrator module."""

from unittest.mock import patch

from ticketplease.main import run_config


def test_run_wizard_with_existing_config():
    """Test that run_wizard does nothing when config already exists."""
    with (
        patch("ticketplease.main.console") as mock_console,
        patch("ticketplease.main.Config") as mock_config_class,
    ):
        # Mock config to simulate existing valid configuration
        mock_config = mock_config_class.return_value
        mock_config.is_first_run.return_value = False
        mock_config.is_configured.return_value = True

        run_config(is_update=False)

        # Verify that no console.print was called (no wizard needed)
        assert mock_console.print.call_count == 0


def test_run_wizard_first_run():
    """Test run_wizard on first run (triggers wizard)."""
    with (
        patch("ticketplease.main.console") as mock_console,
        patch("ticketplease.main.Config") as mock_config_class,
        patch("ticketplease.main.ConfigWizard") as mock_wizard_class,
    ):
        # Mock config to simulate first run
        mock_config = mock_config_class.return_value
        mock_config.is_first_run.return_value = True
        mock_config.is_configured.return_value = False

        # Mock wizard to actually call console.print
        def mock_wizard_run():
            mock_console.print("🎫 Welcome to TicketPlease!")
            return True

        mock_wizard = mock_wizard_class.return_value
        mock_wizard.run.side_effect = mock_wizard_run

        run_config(is_update=False)

        # Verify wizard was instantiated and run
        mock_wizard_class.assert_called_once()
        mock_wizard.run.assert_called_once()

        # Verify welcome message is printed (from wizard)
        calls = mock_console.print.call_args_list
        welcome_messages = [call for call in calls if "🎫 Welcome to TicketPlease!" in str(call)]
        assert len(welcome_messages) >= 1


def test_run_wizard_wizard_cancelled():
    """Test run_wizard when wizard is cancelled."""
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

        run_config(is_update=False)

        # Verify cancellation message was printed
        calls = mock_console.print.call_args_list
        cancel_messages = [call for call in calls if "cancelled" in str(call)]
        assert len(cancel_messages) >= 1
