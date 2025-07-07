"""Tests for the TaskDataCollector module."""

from unittest.mock import MagicMock, patch

import pytest

from config.service import Config
from ticketplease.collector import TaskDataCollector


class TestTaskDataCollector:
    """Test cases for TaskDataCollector."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = MagicMock(spec=Config)
        config.get_platform.return_value = "github"
        config.get_language.return_value = "en"
        config.get_ac_path.return_value = ""
        config.get_dod_path.return_value = ""
        return config

    @pytest.fixture
    def collector(self, mock_config):
        """Create a TaskDataCollector instance."""
        return TaskDataCollector(mock_config)

    def test_init(self, mock_config):
        """Test TaskDataCollector initialization."""
        collector = TaskDataCollector(mock_config)
        assert collector.config == mock_config
        assert "GitHub" in collector.platforms
        assert "Jira" in collector.platforms
        assert "English" in collector.languages
        assert "Español" in collector.languages

    @patch("builtins.input")
    def test_collect_task_description_success(self, mock_input, collector):
        """Test successful task description collection."""
        mock_input.side_effect = ["Create a login form", "DONE"]

        result = collector._collect_task_description()

        assert result == "Create a login form"

    @patch("builtins.input")
    def test_collect_task_description_cancelled(self, mock_input, collector):
        """Test task description collection when cancelled."""
        mock_input.side_effect = KeyboardInterrupt("Task generation cancelled")

        with pytest.raises(KeyboardInterrupt, match="Task generation cancelled"):
            collector._collect_task_description()

    @patch("questionary.select")
    def test_collect_platform_success(self, mock_select, collector):
        """Test successful platform collection."""
        mock_select.return_value.ask.return_value = "Jira"

        result = collector._collect_platform()

        assert result == "jira"
        mock_select.assert_called_once()

    @patch("questionary.select")
    def test_collect_platform_cancelled(self, mock_select, collector):
        """Test platform collection when cancelled."""
        mock_select.return_value.ask.return_value = None

        with pytest.raises(KeyboardInterrupt, match="Task generation cancelled"):
            collector._collect_platform()

    @patch("questionary.select")
    def test_collect_language_success(self, mock_select, collector):
        """Test successful language collection."""
        mock_select.return_value.ask.return_value = "Español"

        result = collector._collect_language()

        assert result == "es"
        mock_select.assert_called_once()

    @patch("questionary.text")
    @patch("questionary.select")
    def test_collect_acceptance_criteria_manual_success(self, mock_select, mock_text, collector):
        """Test successful manual acceptance criteria collection."""
        mock_select.return_value.ask.return_value = "📝 Enter manually"
        mock_text.return_value.ask.side_effect = [
            "User can login",
            "System validates credentials",
            "Error messages are shown",
            "",  # Empty line to finish
        ]

        result = collector._collect_acceptance_criteria()

        assert len(result) == 3
        assert "User can login" in result
        assert "System validates credentials" in result
        assert "Error messages are shown" in result

    @patch("questionary.select")
    def test_collect_acceptance_criteria_manual_cancelled(self, mock_select, collector):
        """Test manual acceptance criteria collection when cancelled."""
        mock_select.return_value.ask.return_value = None

        with pytest.raises(KeyboardInterrupt, match="Task generation cancelled"):
            collector._collect_acceptance_criteria()

    @patch("ticketplease.collector.read_file_content")
    @patch("questionary.path")
    @patch("questionary.select")
    def test_collect_acceptance_criteria_from_file_success(
        self, mock_select, mock_path, mock_read, collector
    ):
        """Test successful acceptance criteria collection from file."""
        mock_select.return_value.ask.return_value = "📁 Load from file"
        mock_path.return_value.ask.return_value = "/path/to/file.txt"
        mock_read.return_value = ["Criterion 1", "Criterion 2"]

        result = collector._collect_acceptance_criteria()

        assert len(result) == 2
        assert "Criterion 1" in result
        assert "Criterion 2" in result
        mock_read.assert_called_once_with("/path/to/file.txt")

    @patch("ticketplease.collector.validate_file_path")
    @patch("ticketplease.collector.read_file_content")
    @patch("questionary.confirm")
    @patch("questionary.select")
    def test_collect_acceptance_criteria_with_default_file(
        self, mock_select, mock_confirm, mock_read, mock_validate, collector
    ):
        """Test acceptance criteria collection with default file."""
        # Setup mocks
        collector.config.get_ac_path.return_value = "/path/to/ac.txt"
        mock_validate.return_value = True
        mock_confirm.return_value.ask.return_value = True
        mock_read.return_value = ["AC 1", "AC 2"]

        result = collector._collect_acceptance_criteria()

        assert len(result) == 2
        assert "AC 1" in result
        assert "AC 2" in result
        mock_confirm.assert_called_once()
        mock_read.assert_called_once_with("/path/to/ac.txt")

    @patch("questionary.select")
    def test_collect_acceptance_criteria_skip(self, mock_select, collector):
        """Test acceptance criteria collection when skipped."""
        mock_select.return_value.ask.return_value = "⏭️  Skip (no criteria)"

        result = collector._collect_acceptance_criteria()

        assert result == []

    @patch("ticketplease.collector.validate_file_path")
    @patch("ticketplease.collector.read_file_content")
    @patch("questionary.confirm")
    @patch("questionary.select")
    def test_collect_definition_of_done_with_default_file(
        self, mock_select, mock_confirm, mock_read, mock_validate, collector
    ):
        """Test definition of done collection with default file."""
        # Setup mocks
        collector.config.get_dod_path.return_value = "/path/to/dod.txt"
        mock_validate.return_value = True
        mock_confirm.return_value.ask.return_value = True
        mock_read.return_value = ["DoD 1", "DoD 2"]

        result = collector._collect_definition_of_done()

        assert len(result) == 2
        assert "DoD 1" in result
        assert "DoD 2" in result
        mock_confirm.assert_called_once()
        mock_read.assert_called_once_with("/path/to/dod.txt")
