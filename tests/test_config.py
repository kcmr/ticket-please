"""Tests for the configuration module."""

from pathlib import Path
from unittest.mock import patch

from services.config import Config


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

    @patch("services.config.Path.exists")
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

    def test_get_model(self) -> None:
        """Test getting model from config."""
        config = Config()
        config._config = {"llm": {"model": "claude-3-sonnet"}}

        assert config.get_model() == "claude-3-sonnet"
