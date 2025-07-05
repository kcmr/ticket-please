"""Tests for the TaskGenerator module."""

from unittest.mock import MagicMock, patch

import pytest

from ai.service import AIService
from config.service import Config
from ticketplease.generator import TaskGenerator


class TestTaskGenerator:
    """Test cases for TaskGenerator."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = MagicMock(spec=Config)
        config.is_configured.return_value = True
        config.get_provider.return_value = "openai"
        config.get_api_key.return_value = "test-api-key"
        config.get_model.return_value = "gpt-4o-mini"
        return config

    @pytest.fixture
    def mock_collector(self):
        """Create a mock task data collector."""
        collector = MagicMock()
        collector.collect_task_data.return_value = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login", "Validation works"],
            "definition_of_done": ["Code reviewed", "Tests pass"],
        }
        return collector

    @pytest.fixture
    def generator(self, mock_config):
        """Create a TaskGenerator instance."""
        return TaskGenerator(mock_config)

    def test_init(self, mock_config):
        """Test TaskGenerator initialization."""
        generator = TaskGenerator(mock_config)
        assert generator.config == mock_config
        assert generator.collector is not None

    @patch("ticketplease.generator.TaskDataCollector")
    def test_generate_task_not_configured(self, mock_collector_class, mock_config):
        """Test task generation when configuration is incomplete."""
        mock_config.is_configured.return_value = False
        generator = TaskGenerator(mock_config)

        result = generator.generate_task()

        assert result is False
        mock_collector_class.assert_called_once_with(mock_config)

    @patch("ticketplease.generator.TaskDataCollector")
    @patch("ticketplease.generator.AIService")
    def test_generate_task_success(self, mock_ai_service_class, mock_collector_class, mock_config):
        """Test successful task generation."""
        # Setup mocks
        mock_collector = MagicMock()
        mock_collector.collect_task_data.return_value = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login"],
            "definition_of_done": ["Code reviewed"],
        }
        mock_collector_class.return_value = mock_collector

        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.return_value = "Generated description"
        mock_ai_service_class.return_value = mock_ai_service

        generator = TaskGenerator(mock_config)

        with patch.object(generator, "_handle_result", return_value=True):
            result = generator.generate_task()

        assert result is True
        mock_collector.collect_task_data.assert_called_once()
        mock_ai_service.generate_task_description.assert_called_once()

    @patch("ticketplease.generator.TaskDataCollector")
    def test_generate_task_cancelled(self, mock_collector_class, mock_config):
        """Test task generation when cancelled by user."""
        mock_collector = MagicMock()
        mock_collector.collect_task_data.side_effect = KeyboardInterrupt()
        mock_collector_class.return_value = mock_collector

        generator = TaskGenerator(mock_config)

        result = generator.generate_task()

        assert result is False

    @patch("ticketplease.generator.TaskDataCollector")
    def test_generate_task_exception(self, mock_collector_class, mock_config):
        """Test task generation when an exception occurs."""
        mock_collector = MagicMock()
        mock_collector.collect_task_data.side_effect = Exception("Test error")
        mock_collector_class.return_value = mock_collector

        generator = TaskGenerator(mock_config)

        result = generator.generate_task()

        assert result is False

    def test_create_ai_service_success(self, generator):
        """Test successful AI service creation."""
        ai_service = generator._create_ai_service()

        assert isinstance(ai_service, AIService)

    def test_create_ai_service_no_api_key(self, mock_config):
        """Test AI service creation when API key is missing."""
        mock_config.get_api_key.return_value = None
        generator = TaskGenerator(mock_config)

        with pytest.raises(ValueError, match="API key not found"):
            generator._create_ai_service()

    @patch("ticketplease.generator.AIService")
    def test_generate_description_success(self, mock_ai_service_class, generator):
        """Test successful description generation."""
        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.return_value = "  Generated description  "

        task_data = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login"],
            "definition_of_done": ["Code reviewed"],
        }

        result = generator._generate_description(mock_ai_service, task_data)

        assert result == "Generated description"
        mock_ai_service.generate_task_description.assert_called_once_with(
            task_description="Create a login form",
            acceptance_criteria=["User can login"],
            definition_of_done=["Code reviewed"],
            platform="github",
            language="en",
        )

    @patch("ticketplease.generator.AIService")
    def test_generate_description_failure(self, mock_ai_service_class, generator):
        """Test description generation failure."""
        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.side_effect = Exception("AI error")

        task_data = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login"],
            "definition_of_done": ["Code reviewed"],
        }

        result = generator._generate_description(mock_ai_service, task_data)

        assert result == ""

    @patch("questionary.select")
    def test_get_user_action_accept(self, mock_select, generator):
        """Test user action selection - accept."""
        mock_select.return_value.ask.return_value = "✅ Accept and copy to clipboard"

        result = generator._get_user_action()

        assert result == "✅ Accept and copy to clipboard"

    @patch("questionary.select")
    def test_get_user_action_refine(self, mock_select, generator):
        """Test user action selection - refine."""
        mock_select.return_value.ask.return_value = "🔄 Refine description"

        result = generator._get_user_action()

        assert result == "🔄 Refine description"

    @patch("questionary.select")
    def test_get_user_action_cancel(self, mock_select, generator):
        """Test user action selection - cancel."""
        mock_select.return_value.ask.return_value = "❌ Cancel"

        result = generator._get_user_action()

        assert result == "❌ Cancel"

    @patch("ticketplease.generator.copy_to_clipboard")
    def test_copy_and_finish_success(self, mock_copy, generator):
        """Test successful copy and finish."""
        mock_copy.return_value = True

        result = generator._copy_and_finish("Test description")

        assert result is True
        mock_copy.assert_called_once_with("Test description")

    @patch("ticketplease.generator.copy_to_clipboard")
    def test_copy_and_finish_failure(self, mock_copy, generator):
        """Test copy and finish when clipboard fails."""
        mock_copy.return_value = False

        result = generator._copy_and_finish("Test description")

        assert result is True  # Still returns True, just shows the description
        mock_copy.assert_called_once_with("Test description")

    @patch("questionary.text")
    def test_refine_description_success(self, mock_text, generator):
        """Test successful description refinement."""
        mock_text.return_value.ask.return_value = "Make it shorter"

        mock_ai_service = MagicMock()
        mock_ai_service.refine_task_description.return_value = "  Refined description  "

        result = generator._refine_description(mock_ai_service, "Original description")

        assert result == "Refined description"
        mock_ai_service.refine_task_description.assert_called_once_with(
            "Original description", "Make it shorter"
        )

    @patch("questionary.text")
    def test_refine_description_cancelled(self, mock_text, generator):
        """Test description refinement when cancelled."""
        mock_text.return_value.ask.return_value = None

        mock_ai_service = MagicMock()

        result = generator._refine_description(mock_ai_service, "Original description")

        assert result == "Original description"
        mock_ai_service.refine_task_description.assert_not_called()

    @patch("questionary.text")
    def test_refine_description_failure(self, mock_text, generator):
        """Test description refinement when AI fails."""
        mock_text.return_value.ask.return_value = "Make it shorter"

        mock_ai_service = MagicMock()
        mock_ai_service.refine_task_description.side_effect = Exception("AI error")

        result = generator._refine_description(mock_ai_service, "Original description")

        assert result == "Original description"

    @patch("questionary.select")
    def test_handle_result_accept(self, mock_select, generator):
        """Test result handling when user accepts."""
        mock_select.return_value.ask.return_value = "✅ Accept and copy to clipboard"

        with (
            patch.object(generator, "_display_result"),
            patch.object(generator, "_copy_and_finish", return_value=True) as mock_copy,
        ):
            result = generator._handle_result(MagicMock(), "Test description")

            assert result is True
            mock_copy.assert_called_once_with("Test description")

    @patch("questionary.select")
    def test_handle_result_cancel(self, mock_select, generator):
        """Test result handling when user cancels."""
        mock_select.return_value.ask.return_value = "❌ Cancel"

        with patch.object(generator, "_display_result"):
            result = generator._handle_result(MagicMock(), "Test description")

            assert result is False

    @patch("questionary.select")
    def test_handle_result_refine_then_accept(self, mock_select, generator):
        """Test result handling with refinement then accept."""
        # First call returns refine, second call returns accept
        mock_select.return_value.ask.side_effect = [
            "🔄 Refine description",
            "✅ Accept and copy to clipboard",
        ]

        with (
            patch.object(generator, "_display_result"),
            patch.object(generator, "_refine_description", return_value="Refined") as mock_refine,
            patch.object(generator, "_copy_and_finish", return_value=True) as mock_copy,
        ):
            result = generator._handle_result(MagicMock(), "Original")

            assert result is True
            mock_refine.assert_called_once()
            mock_copy.assert_called_once_with("Refined")
