"""Tests for the utils module."""

import os
import tempfile
from unittest.mock import patch

from ticketplease.utils import (
    copy_to_clipboard,
    expand_file_path,
    format_acceptance_criteria,
    format_definition_of_done,
    read_file_content,
    validate_file_path,
)


class TestExpandFilePath:
    """Test expand_file_path function."""

    def test_expand_empty_path(self) -> None:
        """Test expanding empty path."""
        assert expand_file_path("") == ""
        assert expand_file_path("   ") == ""

    def test_expand_home_directory(self) -> None:
        """Test expanding home directory."""
        home_path = expand_file_path("~/test.txt")
        expected = os.path.join(os.path.expanduser("~"), "test.txt")
        assert home_path == os.path.abspath(expected)

    def test_expand_relative_path(self) -> None:
        """Test expanding relative path."""
        relative_path = expand_file_path("./test.txt")
        expected = os.path.abspath("./test.txt")
        assert relative_path == expected

    def test_expand_absolute_path(self) -> None:
        """Test expanding already absolute path."""
        abs_path = "/tmp/test.txt"
        result = expand_file_path(abs_path)
        assert result == abs_path


class TestCopyToClipboard:
    """Test copy_to_clipboard function."""

    @patch("ticketplease.utils.pyperclip.copy")
    def test_copy_success(self, mock_copy) -> None:
        """Test successful copy to clipboard."""
        mock_copy.return_value = None
        result = copy_to_clipboard("test text")
        assert result is True
        mock_copy.assert_called_once_with("test text")

    @patch("ticketplease.utils.pyperclip.copy")
    def test_copy_failure(self, mock_copy) -> None:
        """Test failed copy to clipboard."""
        mock_copy.side_effect = Exception("Copy failed")
        result = copy_to_clipboard("test text")
        assert result is False


class TestReadFileContent:
    """Test read_file_content function."""

    def test_read_existing_file(self) -> None:
        """Test reading an existing file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("line 1\nline 2\n\nline 4\n")
            temp_path = f.name

        try:
            content = read_file_content(temp_path)
            assert content == ["line 1", "line 2", "line 4"]
        finally:
            os.unlink(temp_path)

    def test_read_nonexistent_file(self) -> None:
        """Test reading a non-existent file."""
        content = read_file_content("/nonexistent/file.txt")
        assert content == []

    def test_read_empty_file(self) -> None:
        """Test reading an empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            content = read_file_content(temp_path)
            assert content == []
        finally:
            os.unlink(temp_path)

    def test_read_file_with_home_path(self) -> None:
        """Test reading file with ~ in path."""
        # Create a temporary file in home directory for testing
        home_dir = os.path.expanduser("~")
        test_file = os.path.join(home_dir, "test_ticketplease.txt")

        try:
            with open(test_file, "w") as f:
                f.write("test content\n")

            # Use ~ in path
            content = read_file_content("~/test_ticketplease.txt")
            assert content == ["test content"]
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)


class TestValidateFilePath:
    """Test validate_file_path function."""

    def test_validate_existing_file(self) -> None:
        """Test validating an existing file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            assert validate_file_path(temp_path) is True
        finally:
            os.unlink(temp_path)

    def test_validate_nonexistent_file(self) -> None:
        """Test validating a non-existent file."""
        assert validate_file_path("/nonexistent/file.txt") is False

    def test_validate_directory(self) -> None:
        """Test validating a directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            assert validate_file_path(temp_dir) is False

    def test_validate_file_with_home_path(self) -> None:
        """Test validating file with ~ in path."""
        # Create a temporary file in home directory for testing
        home_dir = os.path.expanduser("~")
        test_file = os.path.join(home_dir, "test_validate_ticketplease.txt")

        try:
            with open(test_file, "w") as f:
                f.write("test content")

            # Use ~ in path
            assert validate_file_path("~/test_validate_ticketplease.txt") is True
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)


class TestFormatAcceptanceCriteria:
    """Test format_acceptance_criteria function."""

    def test_format_empty_criteria(self) -> None:
        """Test formatting empty criteria list."""
        result = format_acceptance_criteria([])
        assert result == "No criteria provided"

    def test_format_single_criterion(self) -> None:
        """Test formatting single criterion."""
        criteria = ["User can login"]
        result = format_acceptance_criteria(criteria)
        assert result == "1. User can login"

    def test_format_multiple_criteria(self) -> None:
        """Test formatting multiple criteria."""
        criteria = ["User can login", "User can logout", "User sees dashboard"]
        result = format_acceptance_criteria(criteria)
        expected = "1. User can login\n2. User can logout\n3. User sees dashboard"
        assert result == expected


class TestFormatDefinitionOfDone:
    """Test format_definition_of_done function."""

    def test_format_empty_dod(self) -> None:
        """Test formatting empty DoD list."""
        result = format_definition_of_done([])
        assert result == "No items provided"

    def test_format_single_item(self) -> None:
        """Test formatting single DoD item."""
        items = ["Code reviewed"]
        result = format_definition_of_done(items)
        assert result == "1. Code reviewed"

    def test_format_multiple_items(self) -> None:
        """Test formatting multiple DoD items."""
        items = ["Code reviewed", "Tests written", "Documentation updated"]
        result = format_definition_of_done(items)
        expected = "1. Code reviewed\n2. Tests written\n3. Documentation updated"
        assert result == expected
