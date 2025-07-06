"""Tests for the configuration module."""

from pathlib import Path
from unittest.mock import patch

from config.service import Config


class TestConfig:
    """Test cases for Config class."""

    def test_init(self) -> None:
        """Test Config initialization."""
        config = Config()
        assert config.config_dir == Path.home() / ".config" / "ticketplease"
        assert config.config_file == config.config_dir / "config.toml"

    def test_get_default_config(self) -> None:
        """Test getting default configuration."""
        config = Config()
        default_config = config._get_default_config()

        assert "api_keys" in default_config
        assert "llm" in default_config
        assert "preferences" in default_config

        assert default_config["api_keys"]["provider"] == "openai"
        assert default_config["llm"]["model"] == "gpt-4o-mini"
        assert default_config["preferences"]["default_output_language"] == "es"

    @patch("config.service.Path.exists")
    def test_load_without_existing_file(self, mock_exists) -> None:
        """Test loading config when file doesn't exist."""
        mock_exists.return_value = False
        config = Config()
        result = config.load()

        assert result["api_keys"]["provider"] == "openai"
        assert result["llm"]["model"] == "gpt-4o-mini"

    def test_get_api_key(self) -> None:
        """Test getting API key from config."""
        config = Config()
        config._config = {"api_keys": {"api_key": "test-key"}}

        assert config.get_api_key() == "test-key"

    def test_get_provider(self) -> None:
        """Test getting provider from config."""
        config = Config()
        config._config = {"api_keys": {"provider": "anthropic"}}

        assert config.get_provider() == "anthropic"

    def test_get_ac_path(self) -> None:
        """Test getting acceptance criteria path from config."""
        config = Config()
        config._config = {"preferences": {"default_ac_path": "/path/to/ac.md"}}

        assert config.get_ac_path() == "/path/to/ac.md"

    def test_get_dod_path(self) -> None:
        """Test getting definition of done path from config."""
        config = Config()
        config._config = {"preferences": {"default_dod_path": "/path/to/dod.md"}}

        assert config.get_dod_path() == "/path/to/dod.md"

    def test_is_configured_true(self) -> None:
        """Test is_configured returns True when config is complete."""
        config = Config()
        config._config = {
            "api_keys": {"provider": "openai", "api_key": "sk-test"},
            "llm": {"model": "gpt-4o-mini"},
        }

        assert config.is_configured() is True

    def test_is_configured_false_missing_api_key(self) -> None:
        """Test is_configured returns False when API key is missing."""
        config = Config()
        config._config = {
            "api_keys": {"provider": "openai", "api_key": ""},
            "llm": {"model": "gpt-4o-mini"},
        }

        assert config.is_configured() is False

    def test_is_configured_false_missing_provider(self) -> None:
        """Test is_configured returns False when provider is missing."""
        config = Config()
        config._config = {
            "api_keys": {"provider": "", "api_key": "sk-test"},
            "llm": {"model": "gpt-4o-mini"},
        }

        assert config.is_configured() is False

    @patch("config.service.Path.exists")
    def test_is_first_run_true(self, mock_exists) -> None:
        """Test is_first_run returns True when config file doesn't exist."""
        mock_exists.return_value = False
        config = Config()

        assert config.is_first_run() is True

    @patch("config.service.Path.exists")
    def test_is_first_run_false(self, mock_exists) -> None:
        """Test is_first_run returns False when config file exists."""
        mock_exists.return_value = True
        config = Config()

        assert config.is_first_run() is False

    def test_get_model(self) -> None:
        """Test getting model from config."""
        config = Config()
        config._config = {"llm": {"model": "claude-3-sonnet"}}

        assert config.get_model() == "claude-3-sonnet"
