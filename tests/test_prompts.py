"""Tests for the prompts module."""

from ai.prompts import (
    get_github_format_instructions,
    get_jira_format_instructions,
    get_refinement_prompt,
    get_task_generation_prompt,
)


class TestPrompts:
    """Test cases for prompt functions."""

    def test_get_github_format_instructions(self) -> None:
        """Test GitHub format instructions."""
        instructions = get_github_format_instructions()
        assert "### Description" in instructions
        assert "- [ ]" in instructions
        assert "GitHub Markdown" in instructions

    def test_get_jira_format_instructions(self) -> None:
        """Test Jira format instructions."""
        instructions = get_jira_format_instructions()
        assert "h3. Description" in instructions
        assert "* [criterion" in instructions
        assert "Jira markup" in instructions

    def test_get_task_generation_prompt(self) -> None:
        """Test task generation prompt."""
        prompt = get_task_generation_prompt(
            task_description="Add login feature",
            ac_text="- User can enter credentials\n- User gets logged in",
            dod_text="- Code reviewed\n- Tests pass",
            format_instructions="Format as markdown",
            language="English",
        )

        assert "Add login feature" in prompt
        assert "User can enter credentials" in prompt
        assert "Code reviewed" in prompt
        assert "Format as markdown" in prompt
        assert "English" in prompt

    def test_get_refinement_prompt(self) -> None:
        """Test refinement prompt."""
        prompt = get_refinement_prompt(
            current_description="Current task description",
            refinement_request="Make it more detailed",
        )

        assert "Current task description" in prompt
        assert "Make it more detailed" in prompt
        assert "refine" in prompt.lower()
