# LLM Agent Testbed

This repository serves as an experimental testbed for exploring different types of LLM agents and their capabilities. Using Google's Agent Development Kit (ADK) and LiteLLM, this project provides a framework for testing various agent implementations and use cases.

## Overview

The project aims to:
- Experiment with different LLM agent architectures and capabilities
- Test integration with various LLM providers (currently AWS Bedrock)
- Explore practical applications of LLM agents
- Benchmark performance, capabilities, and limitations

## Getting Started

### Prerequisites

- Python 3.8+
- AWS account with Bedrock access
- Configured AWS credentials

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Agents
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file:
```
# Copy from .env.example and modify as needed
cp .env.example .env
```

### Model Selection

This project uses a simple constant-based model selection system that makes it easy to work with different models based on their capabilities rather than specific identifiers:

```python
# Import models based on their capabilities
from agent_models import FAST_MODEL, SMART_MODEL, POWERFUL_MODEL

# Or use semantic aliases
from agent_models import LITE_MODEL, STANDARD_MODEL, THINKING_MODEL

# Create an agent with the chosen model
agent = LlmAgent(
    name="my_agent",
    model=LiteLlm(model=SMART_MODEL),
    # other parameters...
)
```

You can override the default models by setting environment variables in your `.env` file:
```
AGENT_FAST_MODEL=bedrock/your-preferred-fast-model
AGENT_SMART_MODEL=bedrock/your-preferred-smart-model
AGENT_POWERFUL_MODEL=bedrock/your-preferred-powerful-model
```

### Testing AWS Connection

Verify your AWS Bedrock connectivity:
```bash
python test_bedrock.py
```

This script (`test_bedrock.py`) is a standalone utility that:
- Validates your AWS credentials and environment configuration
- Tests your Bedrock API access by making a simple call to a specified model
- Provides detailed troubleshooting information if connection issues occur
- Uses the model configuration system for selecting which model to test

### Testing OpenSearch Connection

Test your OpenSearch connectivity and agent functionality:
```bash
python test_opensearch.py
```

This script (`test_opensearch.py`):
- Validates your OpenSearch connection settings
- Creates a test index with mapping
- Indexes a sample document
- Performs searches using both direct query and simple text search
- Provides detailed output of each operation

## ADK Commands and Tools

### ADK CLI Commands

Google's Agent Development Kit (ADK) provides a suite of command-line tools to help with agent development:

```bash
# Show all available ADK commands and options
adk --help

# Create a new agent project with prepopulated templates
adk create

# Run your agent interactively in the CLI
adk run

# Start a FastAPI server with Web UI for interactive agent development
adk web

# Deploy your agent to hosted environments
adk deploy

# Evaluate your agent using evaluation sets
adk eval

# Start a FastAPI server for agent API access
adk api_server
```

### ADK Web Interface

The ADK also provides a web interface for interactive development and testing:

```bash
# Start the ADK web interface
adk web
```

The web interface allows you to:
- Interact with your agent in real-time
- View detailed traces of agent execution
- Debug tool calls and responses
- Test different prompts and configurations
- Analyze performance metrics
- Export conversations for future testing

By default, the web interface runs at `http://localhost:8080` and provides a user-friendly dashboard for agent development.

### ADK Configuration

Configure your ADK project by editing the `adk.yaml` file in your project root:

```yaml
project_id: your-project-id
agent_name: your-agent-name
region: your-region
model: your-model-id
```

## Current Implementations

### Weather and Time Agent

Located in `test-agent/agent.py`, this first implementation provides:
- Weather information for cities (currently limited to New York)
- Current time for cities (currently limited to New York)
- Uses Claude 3.5 Sonnet via AWS Bedrock

This initial agent serves as a proof of concept and verification that the framework functions correctly.

### OpenSearch Agent

Located in `opensearch_agent/agent.py`, this implementation provides:
- Connection to OpenSearch clusters
- Index creation with custom mappings
- Document indexing with optional ID specification
- Document search using OpenSearch Query DSL
- Simple text-based search with automatic query generation
- Document deletion by ID

The OpenSearch agent demonstrates how to integrate external data stores with LLM agents to enable semantic search and data management capabilities.

### Claude Code Repository Agent

Located in `cc_repo_agent/agent.py`, this implementation provides:
- Integration with the Claude Code CLI to analyze repositories
- Code search functionality to find patterns and concepts in codebases
- Code explanation capability to understand files or specific code sections
- Code modification tools to implement changes based on instructions
- General task execution for repository-related operations

The Claude Code Repository Agent demonstrates how to leverage Claude's advanced code understanding capabilities within an agent framework to interact with code repositories.

#### Testing the Claude Code Repository Agent

Test your Claude Code Repository Agent setup with a local repository:
```bash
python -m cc_repo_agent.test --repo-path /path/to/your/repository
```

This test script:
- Verifies that Claude Code CLI is properly installed
- Tests access to the specified repository
- Runs a simple Claude Code query against the repository
- Tests the agent's search functionality

**Prerequisites:**
- Claude Code CLI must be installed (`npm install -g @anthropic-ai/claude-code`)
- A local code repository to test with

If you use a custom alias for Claude Code (like `cc`), you can configure it by setting the `CLAUDE_CODE_CMD` environment variable in your `.env` file:
```
CLAUDE_CODE_CMD=cc
```

You can also set the repository path in your `.env` file for ADK web integration:
```
CC_REPO_AGENT_PATH=/path/to/your/repository
```

### GitHub MCP Agent

Located in `github_agent/agent.py`, this agent interacts with GitHub using the official [GitHub MCP Server](https://github.com/github/github-mcp-server).
- Connects to the GitHub MCP Server, which runs as a Docker container.
- Requires a GitHub Personal Access Token (PAT) for authentication, configured via the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable.
- Allows the agent to use tools dynamically provided by the GitHub MCP server for various GitHub operations (e.g., managing issues, repositories, pull requests).
- Configuration for the server (like specific toolsets or GitHub Enterprise Server URLs) can also be managed via environment variables. Refer to `github_agent/README.md` for details.

This agent demonstrates using ADK's `MCPToolset` to integrate with external MCP-compliant servers, enabling interaction with services like GitHub through a standardized protocol.

## Future Work

- Implement additional agent types and capabilities
- Add support for more LLM providers
- Create benchmark tools to compare agent performance
- Explore multi-agent interactions and collaborations