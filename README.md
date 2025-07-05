# TicketPlease

CLI assistant for generating standardized task descriptions using AI.

## Overview

TicketPlease is a command-line tool that helps developers and engineers generate high-quality, standardized task descriptions for platforms like Jira and GitHub using AI. It provides an interactive flow to collect key requirements and produces formatted text ready to copy and paste.

## Features

- **Interactive Guided Flow**: Step-by-step questions to collect all necessary information
- **AI-Powered Content Generation**: Uses LLMs to process user responses and generate complete, well-formatted descriptions
- **Multi-Platform Support**: Generates output in Markdown for GitHub or Jira text markup format
- **Guided Initial Setup**: Onboarding wizard for API key and AI model configuration
- **Persistent Preferences**: Saves user preferences for language, file paths, and platform
- **Iterative Refinement**: Allows users to request modifications to generated text
- **Multilingual Support**: Accepts input in user's language and generates output in configured language
- **Clipboard Integration**: Automatically copies final text to clipboard for immediate use

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/kcmr/ticket-please.git
cd ticket-please
```

2. Setup the development environment:
```bash
make setup
```

3. Install the package in development mode:
```bash
make dev-install
```

## Usage

### Basic Usage

```bash
# Start the interactive task generation flow
tkp

# Show version
tkp --version

# Show help
tkp --help
```

### Configuration

On first use, TicketPlease will guide you through the initial setup:

1. Choose your AI provider (OpenAI, Anthropic, Gemini, OpenRouter)
2. Enter your API key
3. Select an AI model
4. Configure default preferences

Configuration is stored in `~/.config/ticketplease/config.toml`.

## Development

### Available Commands

```bash
# Setup development environment
make setup

# Format code
make format

# Lint code
make lint



# Run tests
make test

# Run tests with coverage
make test-cov

# Run all checks (format, lint, test)
make check

# Clean build artifacts
make clean
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the development checks: `make check`
5. Commit your changes using conventional commits
6. Push to your fork and create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
