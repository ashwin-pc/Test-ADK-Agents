"""
Simple constants for model selection in agent applications.
These can be overridden by environment variables.
"""
import os

# Default model settings - Simple, easy to update in one place
DEFAULT_FAST_MODEL = "bedrock/anthropic.claude-3-haiku-20240307-v1:0"
DEFAULT_SMART_MODEL = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0" 
DEFAULT_POWERFUL_MODEL = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"

# Environment variable overrides - allows changing models without code changes
FAST_MODEL = os.environ.get("AGENT_FAST_MODEL", DEFAULT_FAST_MODEL)
SMART_MODEL = os.environ.get("AGENT_SMART_MODEL", DEFAULT_SMART_MODEL)
POWERFUL_MODEL = os.environ.get("AGENT_POWERFUL_MODEL", DEFAULT_POWERFUL_MODEL)

# Convenience aliases for different use cases
LITE_MODEL = FAST_MODEL
STANDARD_MODEL = SMART_MODEL
THINKING_MODEL = POWERFUL_MODEL