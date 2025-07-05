"""Tests for the configuration update functionality."""

from unittest.mock import patch

from config.service import Config
from config.wizard import ConfigWizard
from ticketplease.main import run_config_update


class TestConfigUpdate:
    """Test cases for configuration update functionality."""

    @patch("questionary.select")
    @patch("questionary.password")
    @patch("questionary.path")
    def test_run_config_update_no_config_launches_wizard(
        self, mock_path, mock_password, mock_select, capsys
    ) -> None:
        """Test config update when no configuration exists - should launch wizard."""
        # Mock user inputs for initial setup
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            "gpt-4o-mini",  # model
            "English",  # language
            "GitHub",  # platform
        ]
        mock_password.return_value.ask.return_value = "test-api-key"
        mock_path.return_value.ask.side_effect = ["", ""]  # empty paths for optional files

        with (
            patch.object(Config, "is_first_run", return_value=True),
            patch.object(Config, "save") as mock_save,
        ):
            run_config_update()

            # Verify save was called (wizard completed successfully)
            mock_save.assert_called_once()

        captured = capsys.readouterr()
        assert "No configuration found. Launching initial setup wizard" in captured.out
        assert "Configuration completed successfully" in captured.out

    @patch("questionary.select")
    @patch("questionary.password")
    @patch("questionary.path")
    def test_run_config_update_success(self, mock_path, mock_password, mock_select, capsys) -> None:
        """Test successful config update."""
        # Mock existing configuration
        mock_config = {
            "api_keys": {"provider": "openai", "api_key": "old-key"},
            "llm": {"model": "gpt-4o-mini"},
            "preferences": {
                "default_output_language": "en",
                "default_platform": "github",
                "default_ac_path": "",
                "default_dod_path": "",
            },
        }

        with (
            patch.object(Config, "is_first_run", return_value=False),
            patch.object(Config, "load", return_value=mock_config),
            patch.object(Config, "save") as mock_save,
        ):
            # Mock user selections
            mock_select.return_value.ask.side_effect = [
                "🤖 AI Provider & Model",  # Update choice
                "OpenAI",  # Provider
                "gpt-4o",  # Model
            ]
            mock_password.return_value.ask.return_value = "new-api-key"

            run_config_update()

            # Verify save was called
            mock_save.assert_called_once()

        captured = capsys.readouterr()
        assert "Configuration updated successfully" in captured.out

    @patch("questionary.select")
    def test_run_config_update_cancelled(self, mock_select, capsys) -> None:
        """Test config update when user cancels."""
        mock_config = {
            "api_keys": {"provider": "openai", "api_key": "test-key"},
            "llm": {"model": "gpt-4o-mini"},
            "preferences": {
                "default_output_language": "en",
                "default_platform": "github",
                "default_ac_path": "",
                "default_dod_path": "",
            },
        }

        with (
            patch.object(Config, "is_first_run", return_value=False),
            patch.object(Config, "load", return_value=mock_config),
        ):
            # Mock user cancellation
            mock_select.return_value.ask.return_value = "❌ Cancel"

            run_config_update()

        captured = capsys.readouterr()
        assert "Configuration update cancelled" in captured.out

    def test_run_config_update_keyboard_interrupt(self, capsys) -> None:
        """Test config update when user interrupts with Ctrl+C."""
        mock_config = {
            "api_keys": {"provider": "openai", "api_key": "test-key"},
            "llm": {"model": "gpt-4o-mini"},
            "preferences": {
                "default_output_language": "en",
                "default_platform": "github",
                "default_ac_path": "",
                "default_dod_path": "",
            },
        }

        with (
            patch.object(Config, "is_first_run", return_value=False),
            patch.object(Config, "load", return_value=mock_config),
            patch.object(ConfigWizard, "run_update", side_effect=KeyboardInterrupt),
        ):
            run_config_update()

        captured = capsys.readouterr()
        assert "Configuration update cancelled" in captured.out

    def test_run_config_update_no_config_keyboard_interrupt(self, capsys) -> None:
        """Test config update when no config exists and user interrupts wizard."""
        with (
            patch.object(Config, "is_first_run", return_value=True),
            patch.object(ConfigWizard, "run", side_effect=KeyboardInterrupt),
        ):
            run_config_update()

        captured = capsys.readouterr()
        assert "No configuration found. Launching initial setup wizard" in captured.out
        assert "Configuration cancelled" in captured.out


class TestConfigWizardUpdate:
    """Test cases for ConfigWizard update methods."""

    def test_show_current_config(self, capsys) -> None:
        """Test showing current configuration."""
        wizard = ConfigWizard()

        # Mock config values
        with (
            patch.object(wizard.config, "get_provider", return_value="openai"),
            patch.object(wizard.config, "get_model", return_value="gpt-4o"),
            patch.object(wizard.config, "get_language", return_value="en"),
            patch.object(wizard.config, "get_platform", return_value="github"),
            patch.object(wizard.config, "get_ac_path", return_value=""),
            patch.object(wizard.config, "get_dod_path", return_value=""),
        ):
            wizard._show_current_config()

        captured = capsys.readouterr()
        assert "Current Configuration:" in captured.out
        assert "Provider: OpenAI" in captured.out
        assert "Model: gpt-4o" in captured.out
        assert "Language: English" in captured.out
        assert "Platform: GitHub" in captured.out

    def test_get_provider_display_name(self) -> None:
        """Test provider display name mapping."""
        wizard = ConfigWizard()

        assert wizard._get_provider_display_name("openai") == "OpenAI"
        assert wizard._get_provider_display_name("anthropic") == "Anthropic"
        assert wizard._get_provider_display_name("gemini") == "Google (Gemini)"
        assert wizard._get_provider_display_name("openrouter") == "OpenRouter"
        assert wizard._get_provider_display_name("unknown") == "unknown"

    def test_get_language_display_name(self) -> None:
        """Test language display name mapping."""
        wizard = ConfigWizard()

        assert wizard._get_language_display_name("en") == "English"
        assert wizard._get_language_display_name("es") == "Español"
        assert wizard._get_language_display_name("unknown") == "unknown"

    def test_get_platform_display_name(self) -> None:
        """Test platform display name mapping."""
        wizard = ConfigWizard()

        assert wizard._get_platform_display_name("github") == "GitHub"
        assert wizard._get_platform_display_name("jira") == "Jira"
        assert wizard._get_platform_display_name("unknown") == "unknown"

    @patch("questionary.select")
    @patch("questionary.password")
    def test_collect_llm_config_with_current(self, mock_password, mock_select) -> None:
        """Test collecting LLM config with current values."""
        wizard = ConfigWizard()

        current_config = {
            "api_keys": {"provider": "anthropic", "api_key": "old-key"},
            "llm": {"model": "claude-3-5-sonnet-latest"},
        }

        mock_select.return_value.ask.side_effect = ["Anthropic", "claude-3-5-haiku-latest"]
        mock_password.return_value.ask.return_value = "new-api-key"

        result = wizard._collect_llm_config(current_config)

        assert result["api_keys"]["provider"] == "anthropic"
        assert result["api_keys"]["api_key"] == "new-api-key"
        assert result["llm"]["model"] == "claude-3-5-haiku-latest"

    @patch("questionary.select")
    def test_collect_preferences_with_current(self, mock_select) -> None:
        """Test collecting preferences with current values."""
        wizard = ConfigWizard()

        current_config = {
            "preferences": {
                "default_output_language": "es",
                "default_platform": "jira",
                "default_ac_path": "/path/to/ac.md",
                "default_dod_path": "/path/to/dod.md",
            }
        }

        with patch.object(
            wizard,
            "_collect_file_paths",
            return_value={"preferences": {"default_ac_path": "", "default_dod_path": ""}},
        ):
            mock_select.return_value.ask.side_effect = ["Español", "Jira"]

            result = wizard._collect_preferences(current_config)

            assert result["preferences"]["default_output_language"] == "es"
            assert result["preferences"]["default_platform"] == "jira"

    @patch("questionary.path")
    def test_collect_file_paths_with_current(self, mock_path) -> None:
        """Test collecting file paths with current values."""
        wizard = ConfigWizard()

        current_config = {
            "preferences": {
                "default_ac_path": "/old/ac.md",
                "default_dod_path": "/old/dod.md",
            }
        }

        mock_path.return_value.ask.side_effect = ["/new/ac.md", "/new/dod.md"]

        with patch("ticketplease.utils.expand_file_path", side_effect=lambda x: x):
            result = wizard._collect_file_paths(current_config)

            assert result["preferences"]["default_ac_path"] == "/new/ac.md"
            assert result["preferences"]["default_dod_path"] == "/new/dod.md"

    @patch("questionary.select")
    def test_run_update_ai_provider_only(self, mock_select) -> None:
        """Test updating only AI provider and model."""
        wizard = ConfigWizard()

        current_config = {
            "api_keys": {"provider": "openai", "api_key": "old-key"},
            "llm": {"model": "gpt-4o-mini"},
            "preferences": {
                "default_output_language": "en",
                "default_platform": "github",
                "default_ac_path": "",
                "default_dod_path": "",
            },
        }

        with (
            patch.object(wizard.config, "load", return_value=current_config.copy()),
            patch.object(wizard.config, "save") as mock_save,
            patch.object(
                wizard,
                "_collect_llm_config",
                return_value={
                    "api_keys": {"provider": "anthropic", "api_key": "new-key"},
                    "llm": {"model": "claude-3-5-sonnet-latest"},
                },
            ),
        ):
            mock_select.return_value.ask.return_value = "🤖 AI Provider & Model"

            result = wizard.run_update()

            assert result is True
            mock_save.assert_called_once()

    @patch("questionary.select")
    def test_run_update_all_settings(self, mock_select) -> None:
        """Test updating all settings."""
        wizard = ConfigWizard()

        current_config = {
            "api_keys": {"provider": "openai", "api_key": "old-key"},
            "llm": {"model": "gpt-4o-mini"},
            "preferences": {
                "default_output_language": "en",
                "default_platform": "github",
                "default_ac_path": "",
                "default_dod_path": "",
            },
        }

        with (
            patch.object(wizard.config, "load", return_value=current_config.copy()),
            patch.object(wizard.config, "save") as mock_save,
            patch.object(
                wizard,
                "_collect_llm_config",
                return_value={
                    "api_keys": {"provider": "anthropic", "api_key": "new-key"},
                    "llm": {"model": "claude-3-5-sonnet-latest"},
                },
            ),
            patch.object(
                wizard,
                "_collect_preferences",
                return_value={
                    "preferences": {
                        "default_output_language": "es",
                        "default_platform": "jira",
                        "default_ac_path": "",
                        "default_dod_path": "",
                    }
                },
            ),
        ):
            mock_select.return_value.ask.return_value = "🔄 Update All Settings"

            result = wizard.run_update()

            assert result is True
            mock_save.assert_called_once()
