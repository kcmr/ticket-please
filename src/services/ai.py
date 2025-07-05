"""AI integration module for TicketPlease."""

import litellm


class AIService:
    """Service for interacting with AI models."""

    def __init__(self, provider: str, api_key: str, model: str) -> None:
        """Initialize the AI service."""
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self._setup_litellm()

    def _setup_litellm(self) -> None:
        """Setup litellm configuration."""
        litellm.api_key = self.api_key
        litellm.set_verbose = False

    def generate_task_description(
        self,
        task_description: str,
        acceptance_criteria: list[str],
        definition_of_done: list[str],
        platform: str,
        language: str,
    ) -> str:
        """Generate a task description using AI."""
        prompt = self._build_prompt(
            task_description,
            acceptance_criteria,
            definition_of_done,
            platform,
            language,
        )

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"Error generating task description: {e}") from e

    def refine_task_description(self, current_description: str, refinement_request: str) -> str:
        """Refine an existing task description."""
        prompt = f"""Please refine the following task description based on the user's request:

Current description:
{current_description}

User's refinement request:
{refinement_request}

Please provide the refined description:"""

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"Error refining task description: {e}") from e

    def _build_prompt(
        self,
        task_description: str,
        acceptance_criteria: list[str],
        definition_of_done: list[str],
        platform: str,
        language: str,
    ) -> str:
        """Build the prompt for task description generation."""
        ac_text = "\n".join(f"- {criterion}" for criterion in acceptance_criteria)
        dod_text = "\n".join(f"- {item}" for item in definition_of_done)

        if platform.lower() == "github":
            format_instructions = """
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
        else:  # Jira
            format_instructions = """
Format the output as Jira markup:
h3. Description
[description here]

h3. Acceptance Criteria
* [criterion 1]
* [criterion 2]

h3. Definition of Done
* [item 1]
* [item 2]
"""

        return f"""Generate a professional task description in {language} based on the following information:

Task Description: {task_description}

Acceptance Criteria:
{ac_text}

Definition of Done:
{dod_text}

{format_instructions}

Please generate a clear, professional description that follows the specified format."""
