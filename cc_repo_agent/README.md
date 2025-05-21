# Claude Code Repository Agent

This agent provides capabilities to interact with code repositories using Claude Code as its underlying tool. The agent can help analyze and modify code across repositories using natural language instructions.

## Features

- **Search Repository**: Find code patterns, functions, or concepts across a repository.
- **Explain Code**: Get detailed explanations of specific files or code sections.
- **Modify Code**: Make changes to code based on natural language instructions.
- **Execute General Tasks**: Perform arbitrary tasks within a repository context.

## Requirements

- Claude Code CLI installed and accessible in your PATH
- Python with dependencies in `requirements.txt`
- AWS credentials for accessing Bedrock models (used by Claude)

## Usage

```python
from cc_repo_agent.agent import repo_agent

# Search for specific patterns in a repository
result = repo_agent.tools.search_repository(
    query="find all API endpoints",
    repo_path="/path/to/your/repo",
    file_patterns=["*.py", "*.js"]  # Optional filter
)

# Get an explanation of a specific file
result = repo_agent.tools.explain_code(
    file_path="src/main.py",
    repo_path="/path/to/your/repo",
    line_range="10-20"  # Optional line range
)

# Modify code based on instructions
result = repo_agent.tools.modify_code(
    instruction="Add error handling to the database connection function",
    file_path="src/database.py",
    repo_path="/path/to/your/repo"
)

# Execute a general task
result = repo_agent.tools.execute_task(
    task="Create a new React component for user authentication",
    repo_path="/path/to/your/repo"
)
```

## Testing

To test the Claude Code Repository Agent, run the included test script:

```bash
python test.py --repo-path "/path/to/your/repo"
```

The test will verify:
1. Claude Code CLI installation
2. Repository access permissions
3. Basic Claude Code query functionality

You can specify a custom query with the `--query` parameter to test more specific functionality.