"""Tests for the AI models module."""

from ai.models import ModelProvider


class TestModelProvider:
    """Test cases for ModelProvider class."""

    def test_get_supported_models(self) -> None:
        """Test getting supported models from all providers."""
        models = ModelProvider.get_supported_models()

        # Should have all expected providers
        expected_providers = ["openai", "anthropic", "gemini", "openrouter"]
        assert all(provider in models for provider in expected_providers)

        # Each provider should have models and custom option
        for provider in expected_providers:
            assert len(models[provider]) > 0
            assert "🔧 Specify custom model" in models[provider]

    def test_get_openai_models(self) -> None:
        """Test OpenAI model retrieval and sorting."""
        models = ModelProvider.get_openai_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should prioritize popular models
        popular_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        found_popular = [m for m in models if m in popular_models]
        assert len(found_popular) > 0

        # Should not have fine-tuned models
        assert not any(m.startswith("ft:") for m in models)
        assert not any(m.startswith("omni-") for m in models)

    def test_get_anthropic_models(self) -> None:
        """Test Anthropic model retrieval and sorting."""
        models = ModelProvider.get_anthropic_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have Claude models
        assert any("claude" in model.lower() for model in models)

        # Should prioritize latest models
        if "claude-3-5-sonnet-latest" in models:
            assert models.index("claude-3-5-sonnet-latest") < len(models) // 2

    def test_get_gemini_models(self) -> None:
        """Test Gemini model retrieval and sorting."""
        models = ModelProvider.get_gemini_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have Gemini models
        assert any("gemini" in model.lower() for model in models)

    def test_get_openrouter_models(self) -> None:
        """Test OpenRouter model retrieval and sorting."""
        models = ModelProvider.get_openrouter_models()

        # Should have models and be limited
        assert len(models) <= 15
        assert len(models) > 0

        # Should have provider-prefixed models
        assert any("/" in model for model in models)

        # Should prioritize major providers
        major_providers = ["anthropic", "openai", "google", "meta-llama"]
        found_major = [
            m for m in models if any(provider in m.lower() for provider in major_providers)
        ]
        assert len(found_major) > 0
