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
AWS_PROFILE="your-aws-profile"
AWS_DEFAULT_REGION="your-aws-region"  # Optional if defined in profile
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

## Current Implementations

### Weather and Time Agent

Located in `test-agent/agent.py`, this first implementation provides:
- Weather information for cities (currently limited to New York)
- Current time for cities (currently limited to New York)
- Uses Claude 3.5 Sonnet via AWS Bedrock

This initial agent serves as a proof of concept and verification that the framework functions correctly.

## Future Work

- Implement additional agent types and capabilities
- Add support for more LLM providers
- Create benchmark tools to compare agent performance
- Explore multi-agent interactions and collaborations