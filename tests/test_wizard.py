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
        # Check that we have some Claude models (dynamic loading)
        assert any("claude" in model.lower() for model in wizard.models["anthropic"])
        assert any("gpt" in model.lower() for model in wizard.models["openai"])
        assert any("gemini" in model.lower() for model in wizard.models["gemini"])
        # Check that custom model option is available
        assert "🔧 Specify custom model" in wizard.models["anthropic"]
        assert "🔧 Specify custom model" in wizard.models["openai"]
        assert "🔧 Specify custom model" in wizard.models["gemini"]
        assert "🔧 Specify custom model" in wizard.models["openrouter"]
        assert "Español" in wizard.languages
        assert "GitHub" in wizard.platforms

    def test_get_openai_models(self) -> None:
        """Test OpenAI model retrieval and sorting."""
        wizard = ConfigWizard()
        models = wizard._get_openai_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should prioritize popular models
        popular_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        found_popular = [m for m in models if m in popular_models]
        assert len(found_popular) > 0

    def test_get_anthropic_models(self) -> None:
        """Test Anthropic model retrieval and sorting."""
        wizard = ConfigWizard()
        models = wizard._get_anthropic_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have Claude models
        assert any("claude" in model.lower() for model in models)

    def test_get_gemini_models(self) -> None:
        """Test Gemini model retrieval and sorting."""
        wizard = ConfigWizard()
        models = wizard._get_gemini_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have Gemini models
        assert any("gemini" in model.lower() for model in models)

    def test_get_openrouter_models(self) -> None:
        """Test OpenRouter model retrieval and sorting."""
        wizard = ConfigWizard()
        models = wizard._get_openrouter_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have provider-prefixed models
        assert any("/" in model for model in models)

    def test_validate_optional_path_empty(self) -> None:
        """Test validation of empty optional path."""
        wizard = ConfigWizard()
        assert wizard._validate_optional_path("") is True

    def test_validate_optional_path_whitespace(self) -> None:
        """Test validation of whitespace-only path."""
        wizard = ConfigWizard()
        assert wizard._validate_optional_path("   ") is True

    def test_validate_optional_path_nonexistent(self) -> None:
        """Test validation of non-existent file path."""
        wizard = ConfigWizard()
        result = wizard._validate_optional_path("/nonexistent/file.txt")
        assert isinstance(result, str)
        assert "does not exist" in result

    def test_validate_optional_path_existing_file(self, tmp_path) -> None:
        """Test validation of existing file path."""
        wizard = ConfigWizard()
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = wizard._validate_optional_path(str(test_file))
        assert result is True

    def test_validate_optional_path_directory(self, tmp_path) -> None:
        """Test validation of directory path (should fail)."""
        wizard = ConfigWizard()
        result = wizard._validate_optional_path(str(tmp_path))
        assert isinstance(result, str)
        assert "not a file" in result

    @patch("questionary.select")
    @patch("questionary.password")
    @patch("questionary.path")
    def test_run_success(self, mock_path, mock_password, mock_select) -> None:
        """Test successful wizard run."""
        # Mock user inputs
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            "gpt-4o-mini",  # model
            "English",  # language
            "GitHub",  # platform
        ]
        mock_password.return_value.ask.return_value = "test-api-key"
        mock_path.return_value.ask.side_effect = ["", ""]  # empty paths for optional files

        # Mock config save
        wizard = ConfigWizard()
        with patch.object(wizard.config, "save", return_value=None):
            result = wizard.run()
            assert result is True

    @patch("questionary.select")
    @patch("questionary.password")
    @patch("questionary.path")
    def test_run_custom_model(self, mock_path, mock_password, mock_select) -> None:
        """Test wizard run with custom model specification."""
        # Mock user inputs
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            "🔧 Specify custom model",  # model choice
            "English",  # language
            "GitHub",  # platform
        ]
        mock_password.return_value.ask.return_value = "test-api-key"
        mock_path.return_value.ask.side_effect = ["", ""]  # empty paths for optional files

        # Mock custom model input
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "gpt-4o-2024-11-20"

            wizard = ConfigWizard()
            with patch.object(wizard.config, "save", return_value=None):
                result = wizard.run()
                assert result is True

    @patch("questionary.select")
    @patch("questionary.password")
    @patch("questionary.path")
    def test_run_save_failure(self, mock_path, mock_password, mock_select) -> None:
        """Test wizard when config save fails."""
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            "gpt-4o-mini",  # model
            "English",  # language
            "GitHub",  # platform
        ]
        mock_password.return_value.ask.return_value = "test-api-key"
        mock_path.return_value.ask.side_effect = ["", ""]  # empty paths

        wizard = ConfigWizard()
        with patch.object(wizard.config, "save", side_effect=Exception("Save failed")):
            # The wizard should re-raise the exception since it doesn't handle save failures
            with pytest.raises(Exception, match="Save failed"):
                wizard.run()

    @patch("questionary.select")
    def test_run_cancelled_provider(self, mock_select) -> None:
        """Test wizard cancellation at provider selection."""
        mock_select.return_value.ask.return_value = None  # User cancels

        wizard = ConfigWizard()
        result = wizard.run()
        assert result is False

    @patch("questionary.select")
    @patch("questionary.password")
    def test_run_cancelled_api_key(self, mock_password, mock_select) -> None:
        """Test wizard cancellation at API key input."""
        mock_select.return_value.ask.return_value = "OpenAI"
        mock_password.return_value.ask.return_value = None  # User cancels

        wizard = ConfigWizard()
        result = wizard.run()
        assert result is False

    @patch("questionary.select")
    @patch("questionary.password")
    def test_run_cancelled_model(self, mock_password, mock_select) -> None:
        """Test wizard cancellation at model selection."""
        mock_select.return_value.ask.side_effect = [
            "OpenAI",  # provider
            None,  # model (user cancels)
        ]
        mock_password.return_value.ask.return_value = "test-api-key"

        wizard = ConfigWizard()
        result = wizard.run()
        assert result is False

    def test_providers_mapping(self) -> None:
        """Test that all providers have correct mappings."""
        wizard = ConfigWizard()
        expected_providers = {
            "OpenAI": "openai",
            "Anthropic": "anthropic",
            "Google (Gemini)": "gemini",
            "OpenRouter": "openrouter",
        }
        assert wizard.providers == expected_providers

    def test_models_structure(self) -> None:
        """Test that models structure is correct."""
        wizard = ConfigWizard()

        # Check that all providers have models
        for provider in wizard.providers.values():
            assert provider in wizard.models
            assert isinstance(wizard.models[provider], list)
            assert len(wizard.models[provider]) > 0

    def test_languages_mapping(self) -> None:
        """Test that languages have correct mappings."""
        wizard = ConfigWizard()
        expected_languages = {
            "Español": "es",
            "English": "en",
        }
        assert wizard.languages == expected_languages

    def test_platforms_mapping(self) -> None:
        """Test that platforms have correct mappings."""
        wizard = ConfigWizard()
        expected_platforms = {
            "GitHub": "github",
            "Jira": "jira",
        }
        assert wizard.platforms == expected_platforms
