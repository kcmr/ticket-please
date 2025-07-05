"""Tests for the configuration wizard module."""

from unittest.mock import patch

import pytest

from config.service import Config
from config.wizard import ConfigWizard


class TestConfigWizard:
    """Test cases for ConfigWizard class."""

    def test_init(self) -> None:
        """Test ConfigWizard initialization."""
        wizard = ConfigWizard()
        assert isinstance(wizard.config, Config)
        assert "OpenAI" in wizard.providers
        assert "openai" in wizard.models
        assert "Español" in wizard.languages
        assert "GitHub" in wizard.platforms

    def test_validate_optional_path_empty(self) -> None:
        """Test validation of empty optional path."""
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("")
        assert result is True

    def test_validate_optional_path_whitespace(self) -> None:
        """Test validation of whitespace-only optional path."""
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("   ")
        assert result is True

    @patch("config.wizard.Path.exists")
    def test_validate_optional_path_nonexistent(self, mock_exists) -> None:
        """Test validation of non-existent file path."""
        mock_exists.return_value = False
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("/nonexistent/file.txt")
        assert isinstance(result, str)
        assert "no existe" in result

    @patch("config.wizard.Path.is_file")
    @patch("config.wizard.Path.exists")
    def test_validate_optional_path_not_file(self, mock_exists, mock_is_file) -> None:
        """Test validation of path that is not a file."""
        mock_exists.return_value = True
        mock_is_file.return_value = False
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("/some/directory")
        assert isinstance(result, str)
        assert "no es un archivo válido" in result

    @patch("config.wizard.Path.is_file")
    @patch("config.wizard.Path.exists")
    def test_validate_optional_path_valid(self, mock_exists, mock_is_file) -> None:
        """Test validation of valid file path."""
        mock_exists.return_value = True
        mock_is_file.return_value = True
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("/valid/file.txt")
        assert result is True

    @patch("config.wizard.questionary.select")
    @patch("config.wizard.questionary.password")
    @patch("config.wizard.questionary.path")
    @patch("config.wizard.console")
    def test_run_complete_flow(self, mock_console, mock_path, mock_password, mock_select) -> None:
        """Test complete wizard flow."""
        # Mock questionary responses
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            "gpt-4o-mini",  # model
            "Español",  # language
            "GitHub",  # platform
        ]
        mock_password.return_value.ask.return_value = "sk-test-key"
        mock_path.return_value.ask.side_effect = ["", ""]  # empty paths

        wizard = ConfigWizard()

        with patch.object(wizard.config, "save") as mock_save:
            result = wizard.run()

            # Verify save was called
            mock_save.assert_called_once()

            # Verify returned config structure
            assert "api_keys" in result
            assert "llm" in result
            assert "preferences" in result

            assert result["api_keys"]["provider"] == "openai"
            assert result["api_keys"]["api_key"] == "sk-test-key"
            assert result["llm"]["model"] == "gpt-4o-mini"
            assert result["preferences"]["default_output_language"] == "es"
            assert result["preferences"]["default_platform"] == "github"

    @patch("config.wizard.questionary.select")
    def test_run_keyboard_interrupt(self, mock_select) -> None:
        """Test wizard handling of keyboard interrupt."""
        mock_select.return_value.ask.return_value = None  # Simulate Ctrl+C

        wizard = ConfigWizard()

        with pytest.raises(KeyboardInterrupt):
            wizard.run()

    @patch("config.wizard.questionary.select")
    @patch("config.wizard.questionary.password")
    def test_collect_llm_config(self, mock_password, mock_select) -> None:
        """Test LLM configuration collection."""
        mock_select.return_value.ask.side_effect = ["Anthropic", "claude-3-5-sonnet-20241022"]
        mock_password.return_value.ask.return_value = "sk-ant-test"

        wizard = ConfigWizard()

        with patch("config.wizard.console"):
            result = wizard._collect_llm_config()

            assert result["api_keys"]["provider"] == "anthropic"
            assert result["api_keys"]["api_key"] == "sk-ant-test"
            assert result["llm"]["model"] == "claude-3-5-sonnet-20241022"

    @patch("config.wizard.questionary.select")
    @patch("config.wizard.questionary.path")
    def test_collect_preferences(self, mock_path, mock_select) -> None:
        """Test preferences collection."""
        mock_select.return_value.ask.side_effect = ["English", "Jira"]
        mock_path.return_value.ask.side_effect = ["/path/to/ac.md", "/path/to/dod.md"]

        wizard = ConfigWizard()

        with patch("config.wizard.console"):
            result = wizard._collect_preferences()

            assert result["preferences"]["default_output_language"] == "en"
            assert result["preferences"]["default_platform"] == "jira"
            assert result["preferences"]["default_ac_path"] == "/path/to/ac.md"
            assert result["preferences"]["default_dod_path"] == "/path/to/dod.md"
