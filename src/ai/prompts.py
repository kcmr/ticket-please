"""Prompts for AI interactions in TicketPlease."""


def get_task_generation_prompt(
    task_description: str,
    ac_text: str,
    dod_text: str,
    format_instructions: str,
    language: str,
) -> str:
    """Generate the prompt for task description generation."""
    return f"""Generate a professional task description in {language} based on the following information:

Task Description: {task_description}

Acceptance Criteria:
{ac_text}

Definition of Done:
{dod_text}

{format_instructions}

Please generate a clear, professional description that follows the specified format."""


def get_refinement_prompt(current_description: str, refinement_request: str) -> str:
    """Generate the prompt for task description refinement."""
    return f"""Please refine the following task description based on the user's request:

Current description:
{current_description}

User's refinement request:
{refinement_request}

Please provide the refined description:"""


def get_github_format_instructions() -> str:
    """Get format instructions for GitHub Markdown."""
    return """
Format the output as GitHub Markdown:
### Description
[description here]

### Acceptance Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]

### Definition of Done
- [ ] [item 1]
- [ ] [item 2]
"""


def get_jira_format_instructions() -> str:
    """Get format instructions for Jira markup."""
    return """
Format the output as Jira markup:
h3. Description
[description here]

h3. Acceptance Criteria
* [criterion 1]
* [criterion 2]

h3. Definition of Done
* [item 1]
* [item 2]

Use Jira text formatting when appropriate:
- For inline code or technical terms: {{monospaced text}}
- For emphasis: *strong text* or _italic text_
- For code blocks: {code}code here{code}
- For file names, commands, or technical references: {{filename.ext}} or {{command}}
"""
