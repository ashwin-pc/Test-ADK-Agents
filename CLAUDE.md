# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository serves as a testbed for experimenting with different types of LLM agents to explore their capabilities. Using Google's Agent Development Kit (ADK) and LiteLLM, this project allows testing various agent implementations and use cases. Key aspects include:
- Integration with AWS Bedrock models via LiteLLM
- Multiple agent implementations to test different capabilities and use cases
- The weather and time agent is just the first implementation to verify the framework works

## Environment Setup

The project requires:
- Python with dependencies in requirements.txt
- AWS credentials for accessing Bedrock models

### Installation

```bash
pip install -r requirements.txt
```

### Environment Configuration

The project expects AWS credentials to be configured. Create a `.env` file in the root directory with:

```
AWS_PROFILE="your-aws-profile"
AWS_DEFAULT_REGION="your-aws-region"  # Optional if already in AWS profile
```

## Running the Test Script

To test AWS Bedrock connectivity and model access:

```bash
python -m test-agent.test
```

This script verifies your AWS configuration and tests a call to a Bedrock model.

## Current Agent Implementation

The first test agent is defined in `test-agent/agent.py` and provides two tools:
- `get_weather(city)`: Returns weather information for a city (currently only supports New York)
- `get_current_time(city)`: Returns current time for a city (currently only supports New York)

This initial agent uses Claude 3.5 Sonnet via AWS Bedrock and serves as a proof of concept for the framework. Future implementations will explore additional agent types, capabilities, and use cases.