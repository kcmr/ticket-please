"""Integration tests for TicketPlease."""

from unittest.mock import MagicMock, patch

import pytest

from config.service import Config
from ticketplease.main import run_task_generation


class TestIntegration:
    """Integration test cases for the complete flow."""

    @pytest.fixture
    def mock_config_configured(self):
        """Create a mock configured configuration."""
        config = MagicMock(spec=Config)
        config.is_configured.return_value = True
        config.get_provider.return_value = "openai"
        config.get_api_key.return_value = "test-api-key"
        config.get_model.return_value = "gpt-4o-mini"
        config.get_platform.return_value = "github"
        config.get_language.return_value = "en"
        config.get_ac_path.return_value = ""
        config.get_dod_path.return_value = ""
        return config

    @patch("ticketplease.main.Config")
    @patch("ticketplease.main.TaskGenerator")
    def test_run_task_generation_success(self, mock_generator_class, mock_config_class):
        """Test successful task generation flow."""
        # Setup mocks
        mock_config = MagicMock()
        mock_config.is_first_run.return_value = False  # Configuration exists
        mock_config_class.return_value = mock_config

        mock_generator = MagicMock()
        mock_generator.generate_task.return_value = True
        mock_generator_class.return_value = mock_generator

        # Run the function
        run_task_generation()

        # Verify calls
        mock_config_class.assert_called_once()
        mock_config.is_first_run.assert_called_once()
        mock_generator_class.assert_called_once_with(mock_config)
        mock_generator.generate_task.assert_called_once()

    @patch("ticketplease.main.Config")
    @patch("ticketplease.main.TaskGenerator")
    def test_run_task_generation_failure(self, mock_generator_class, mock_config_class):
        """Test task generation flow when generation fails."""
        # Setup mocks
        mock_config = MagicMock()
        mock_config.is_first_run.return_value = False  # Configuration exists
        mock_config_class.return_value = mock_config

        mock_generator = MagicMock()
        mock_generator.generate_task.return_value = False
        mock_generator_class.return_value = mock_generator

        # Run the function (should not raise exception)
        run_task_generation()

        # Verify calls
        mock_config_class.assert_called_once()
        mock_config.is_first_run.assert_called_once()
        mock_generator_class.assert_called_once_with(mock_config)
        mock_generator.generate_task.assert_called_once()

    @patch("ticketplease.main.Config")
    @patch("ticketplease.main.console")
    def test_run_task_generation_no_config(self, mock_console, mock_config_class):
        """Test task generation flow when no configuration exists."""
        # Setup mocks
        mock_config = MagicMock()
        mock_config.is_first_run.return_value = True  # No configuration
        mock_config_class.return_value = mock_config

        # Run the function
        run_task_generation()

        # Verify calls
        mock_config_class.assert_called_once()
        mock_config.is_first_run.assert_called_once()

        # Verify console messages were printed
        assert mock_console.print.call_count >= 3  # Should print error and instruction messages

    @patch("ticketplease.generator.TaskDataCollector")
    @patch("ticketplease.generator.AIService")
    @patch("ticketplease.generator.copy_to_clipboard")
    @patch("questionary.text")
    @patch("questionary.select")
    def test_complete_flow_manual_input(
        self,
        mock_select,
        mock_copy,
        mock_ai_service_class,
        mock_collector_class,
        mock_config_configured,
    ):
        """Test complete flow with manual input."""
        # Setup collector mock
        mock_collector = MagicMock()
        mock_collector.collect_task_data.return_value = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login", "Validation works"],
            "definition_of_done": ["Code reviewed", "Tests pass"],
        }
        mock_collector_class.return_value = mock_collector

        # Setup AI service mock
        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.return_value = "Generated task description"
        mock_ai_service_class.return_value = mock_ai_service

        # Setup user interaction mocks
        mock_select.return_value.ask.return_value = "✅ Accept and copy to clipboard"
        mock_copy.return_value = True

        # Import and run
        from ticketplease.generator import TaskGenerator

        generator = TaskGenerator(mock_config_configured)
        result = generator.generate_task()

        # Verify the flow
        assert result is True
        mock_collector.collect_task_data.assert_called_once()
        mock_ai_service.generate_task_description.assert_called_once_with(
            task_description="Create a login form",
            acceptance_criteria=["User can login", "Validation works"],
            definition_of_done=["Code reviewed", "Tests pass"],
            platform="github",
            language="en",
        )
        mock_copy.assert_called_once_with("Generated task description")

    @patch("ticketplease.generator.TaskDataCollector")
    @patch("ticketplease.generator.AIService")
    @patch("ticketplease.generator.copy_to_clipboard")
    @patch("questionary.text")
    @patch("questionary.select")
    def test_complete_flow_with_refinement(
        self,
        mock_select,
        mock_text,
        mock_copy,
        mock_ai_service_class,
        mock_collector_class,
        mock_config_configured,
    ):
        """Test complete flow with description refinement."""
        # Setup collector mock
        mock_collector = MagicMock()
        mock_collector.collect_task_data.return_value = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login"],
            "definition_of_done": ["Code reviewed"],
        }
        mock_collector_class.return_value = mock_collector

        # Setup AI service mock
        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.return_value = "Initial description"
        mock_ai_service.refine_task_description.return_value = "Refined description"
        mock_ai_service_class.return_value = mock_ai_service

        # Setup user interaction mocks - first refine, then accept
        mock_select.return_value.ask.side_effect = [
            "🔄 Make changes",
            "✅ Accept and copy to clipboard",
        ]
        mock_text.return_value.ask.return_value = "Make it shorter"
        mock_copy.return_value = True

        # Import and run
        from ticketplease.generator import TaskGenerator

        generator = TaskGenerator(mock_config_configured)
        result = generator.generate_task()

        # Verify the flow
        assert result is True
        mock_collector.collect_task_data.assert_called_once()
        mock_ai_service.generate_task_description.assert_called_once()
        mock_ai_service.refine_task_description.assert_called_once_with(
            "Initial description", "Make it shorter"
        )
        mock_copy.assert_called_once_with("Refined description")

    @patch("ticketplease.generator.TaskDataCollector")
    @patch("ticketplease.generator.AIService")
    @patch("questionary.select")
    def test_complete_flow_cancelled(
        self,
        mock_select,
        mock_ai_service_class,
        mock_collector_class,
        mock_config_configured,
    ):
        """Test complete flow when user cancels."""
        # Setup collector mock
        mock_collector = MagicMock()
        mock_collector.collect_task_data.return_value = {
            "task_description": "Create a login form",
            "platform": "github",
            "language": "en",
            "acceptance_criteria": ["User can login"],
            "definition_of_done": ["Code reviewed"],
        }
        mock_collector_class.return_value = mock_collector

        # Setup AI service mock
        mock_ai_service = MagicMock()
        mock_ai_service.generate_task_description.return_value = "Generated description"
        mock_ai_service_class.return_value = mock_ai_service

        # Setup user interaction mocks - user cancels
        mock_select.return_value.ask.return_value = "❌ Cancel"

        # Import and run
        from ticketplease.generator import TaskGenerator

        generator = TaskGenerator(mock_config_configured)
        result = generator.generate_task()

        # Verify the flow
        assert result is False
        mock_collector.collect_task_data.assert_called_once()
        mock_ai_service.generate_task_description.assert_called_once()

    @patch("ticketplease.generator.TaskDataCollector")
    def test_complete_flow_not_configured(self, mock_collector_class):
        """Test complete flow when configuration is incomplete."""
        # Setup config mock
        mock_config = MagicMock()
        mock_config.is_configured.return_value = False

        # Import and run
        from ticketplease.generator import TaskGenerator

        generator = TaskGenerator(mock_config)
        result = generator.generate_task()

        # Verify the flow
        assert result is False
        # Collector should be called during initialization
        mock_collector_class.assert_called_once_with(mock_config)

    @patch("ticketplease.generator.TaskDataCollector")
    def test_complete_flow_data_collection_cancelled(
        self, mock_collector_class, mock_config_configured
    ):
        """Test complete flow when data collection is cancelled."""
        # Setup collector mock to raise KeyboardInterrupt
        mock_collector = MagicMock()
        mock_collector.collect_task_data.side_effect = KeyboardInterrupt()
        mock_collector_class.return_value = mock_collector

        # Import and run
        from ticketplease.generator import TaskGenerator

        generator = TaskGenerator(mock_config_configured)
        result = generator.generate_task()

        # Verify the flow
        assert result is False
        mock_collector.collect_task_data.assert_called_once()
