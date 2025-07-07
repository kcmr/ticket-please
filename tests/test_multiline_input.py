"""Tests for multiline input functionality."""

from unittest.mock import Mock, patch

import pytest

from config.service import Config
from ticketplease.collector import TaskDataCollector


class TestMultilineInput:
    """Test multiline input functionality with DONE keyword to finish."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Mock(spec=Config)
        self.config.get_platform.return_value = "github"
        self.config.get_language.return_value = "en"
        self.config.get_ac_path.return_value = None
        self.config.get_dod_path.return_value = None
        self.collector = TaskDataCollector(self.config)

    @patch("builtins.input")
    def test_multiline_input_basic(self, mock_input):
        """Test basic multiline input functionality."""
        mock_input.side_effect = ["This is line 1", "This is line 2", "This is line 3", "DONE"]

        result = self.collector._collect_multiline_input()

        expected = "This is line 1\nThis is line 2\nThis is line 3"
        assert result == expected

    @patch("builtins.input")
    def test_multiline_input_with_empty_lines(self, mock_input):
        """Test multiline input with empty lines."""
        mock_input.side_effect = [
            "First paragraph",
            "",
            "Second paragraph after empty line",
            "DONE",
        ]

        result = self.collector._collect_multiline_input()

        expected = "First paragraph\n\nSecond paragraph after empty line"
        assert result == expected

    @patch("builtins.input")
    @patch("rich.console.Console.print")
    def test_multiline_input_empty_validation(self, mock_print, mock_input):
        """Test that empty multiline input is rejected and re-prompted."""
        # First attempt: only DONE (empty), second attempt: valid input
        mock_input.side_effect = [
            "DONE",  # First attempt - empty
            "Valid description",  # Second attempt
            "DONE",
        ]

        result = self.collector._collect_multiline_input()

        # Should show error message for empty input
        mock_print.assert_any_call("[red]Task description cannot be empty[/red]")
        assert result == "Valid description"

    @patch("builtins.input")
    @patch("rich.console.Console.print")
    def test_multiline_input_whitespace_only_validation(self, mock_print, mock_input):
        """Test that whitespace-only input is rejected and re-prompted."""
        mock_input.side_effect = [
            "   ",  # First attempt - whitespace only
            "  ",
            "DONE",
            "Valid description",  # Second attempt
            "DONE",
        ]

        result = self.collector._collect_multiline_input()

        # Should show error message for empty input
        mock_print.assert_any_call("[red]Task description cannot be empty[/red]")
        assert result == "Valid description"

    @patch("builtins.input")
    def test_multiline_input_keyboard_interrupt(self, mock_input):
        """Test that KeyboardInterrupt is properly handled in multiline input."""
        mock_input.side_effect = KeyboardInterrupt("Task generation cancelled")

        with pytest.raises(KeyboardInterrupt, match="Task generation cancelled"):
            self.collector._collect_multiline_input()

    @patch("builtins.input")
    @patch("rich.console.Console.print")
    def test_multiline_input_eof_handling(self, mock_print, mock_input):
        """Test that EOFError is properly handled in multiline input."""
        mock_input.side_effect = EOFError()

        with pytest.raises(KeyboardInterrupt, match="Task generation cancelled"):
            self.collector._collect_multiline_input()

        # Should show cancellation message
        mock_print.assert_any_call("\n[yellow]Input cancelled[/yellow]")

    @patch("builtins.input")
    def test_multiline_input_strips_whitespace(self, mock_input):
        """Test that multiline input properly strips leading/trailing whitespace."""
        mock_input.side_effect = ["  ", "  Line with content  ", "  ", "DONE"]

        result = self.collector._collect_multiline_input()

        # The final result should be stripped
        expected = "Line with content"
        assert result == expected

    @patch("builtins.input")
    def test_single_line_input_works(self, mock_input):
        """Test that single line input works with the multiline interface."""
        mock_input.side_effect = ["Single line description", "DONE"]

        result = self.collector._collect_multiline_input()

        assert result == "Single line description"

    @patch("builtins.input")
    def test_multiline_input_preserves_internal_formatting(self, mock_input):
        """Test that internal formatting is preserved in multiline input."""
        mock_input.side_effect = ["Line 1", "  Indented line", "Line 3", "DONE"]

        result = self.collector._collect_multiline_input()

        expected = "Line 1\n  Indented line\nLine 3"
        assert result == expected

    @patch("builtins.input")
    def test_done_keyword_case_insensitive(self, mock_input):
        """Test that DONE keyword is case insensitive."""
        mock_input.side_effect = [
            "Test line",
            "done",  # lowercase should work
        ]

        result = self.collector._collect_multiline_input()

        assert result == "Test line"

    @patch("builtins.input")
    def test_done_keyword_with_whitespace(self, mock_input):
        """Test that DONE keyword works with surrounding whitespace."""
        mock_input.side_effect = [
            "Test line",
            "  DONE  ",  # with whitespace should work
        ]

        result = self.collector._collect_multiline_input()

        assert result == "Test line"

    def test_multiline_input_method_exists(self):
        """Test that the multiline input method exists and is callable."""
        assert hasattr(self.collector, "_collect_multiline_input")
        assert callable(self.collector._collect_multiline_input)

    @patch("builtins.input")
    def test_collect_task_description_integration_success(self, mock_input):
        """Test successful task description collection through public interface."""
        mock_input.side_effect = ["Test task description", "DONE"]

        result = self.collector._collect_task_description()

        assert result == "Test task description"

    @patch("builtins.input")
    def test_collect_task_description_integration_multiline(self, mock_input):
        """Test multiline task description collection through public interface."""
        mock_input.side_effect = [
            "This is a multiline",
            "task description",
            "with multiple lines",
            "DONE",
        ]

        result = self.collector._collect_task_description()

        expected = "This is a multiline\ntask description\nwith multiple lines"
        assert result == expected
