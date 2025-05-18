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

## Future Work

- Implement additional agent types and capabilities
- Add support for more LLM providers
- Create benchmark tools to compare agent performance
- Explore multi-agent interactions and collaborations