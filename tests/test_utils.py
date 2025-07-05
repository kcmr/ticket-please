"""Tests for the utils module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from ticketplease.utils import (
    copy_to_clipboard,
    format_acceptance_criteria,
    format_definition_of_done,
    read_file_content,
    validate_file_path,
)


class TestUtils:
    """Test cases for utility functions."""

    def test_format_acceptance_criteria(self) -> None:
        """Test formatting acceptance criteria."""
        criteria = ["User can login", "User can logout"]
        result = format_acceptance_criteria(criteria)
        expected = "1. User can login\n2. User can logout"
        assert result == expected

    def test_format_acceptance_criteria_empty(self) -> None:
        """Test formatting empty acceptance criteria."""
        result = format_acceptance_criteria([])
        assert result == "No criteria provided"

    def test_format_definition_of_done(self) -> None:
        """Test formatting definition of done."""
        items = ["Code reviewed", "Tests pass"]
        result = format_definition_of_done(items)
        expected = "1. Code reviewed\n2. Tests pass"
        assert result == expected

    def test_format_definition_of_done_empty(self) -> None:
        """Test formatting empty definition of done."""
        result = format_definition_of_done([])
        assert result == "No items provided"

    def test_validate_file_path_exists(self) -> None:
        """Test file path validation with existing file."""
        with tempfile.NamedTemporaryFile() as tmp_file:
            result = validate_file_path(tmp_file.name)
            assert result is True

    def test_validate_file_path_not_exists(self) -> None:
        """Test file path validation with non-existing file."""
        result = validate_file_path("/non/existent/file.txt")
        assert result is False

    def test_read_file_content(self) -> None:
        """Test reading file content."""
        content = "Line 1\nLine 2\nLine 3"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_file.flush()

            result = read_file_content(tmp_file.name)
            expected = ["Line 1", "Line 2", "Line 3"]
            assert result == expected

            # Cleanup
            Path(tmp_file.name).unlink()

    def test_read_file_content_empty(self) -> None:
        """Test reading empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            tmp_file.write("")
            tmp_file.flush()

            result = read_file_content(tmp_file.name)
            assert result == []

            # Cleanup
            Path(tmp_file.name).unlink()

    @patch("ticketplease.utils.pyperclip.copy")
    def test_copy_to_clipboard_success(self, mock_copy) -> None:
        """Test successful clipboard copy."""
        result = copy_to_clipboard("test text")
        assert result is True
        mock_copy.assert_called_once_with("test text")

    @patch("ticketplease.utils.pyperclip.copy")
    def test_copy_to_clipboard_failure(self, mock_copy) -> None:
        """Test clipboard copy failure."""
        mock_copy.side_effect = Exception("Clipboard error")
        result = copy_to_clipboard("test text")
        assert result is False
