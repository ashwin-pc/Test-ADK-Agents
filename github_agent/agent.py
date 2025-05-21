import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import sys

# Add the parent directory to sys.path to allow importing agent_models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_models import POWERFUL_MODEL

# Environment variable names
GITHUB_PAT_ENV_VAR = "GITHUB_PERSONAL_ACCESS_TOKEN"
GITHUB_MCP_TOOLSETS_ENV_VAR = "GITHUB_TOOLSETS"
GITHUB_MCP_DYNAMIC_TOOLSETS_ENV_VAR = "GITHUB_DYNAMIC_TOOLSETS"
GITHUB_HOST_ENV_VAR = "GITHUB_HOST"

# Retrieve sensitive information and configurations from environment variables
github_pat = os.environ.get(GITHUB_PAT_ENV_VAR)
github_toolsets = os.environ.get(GITHUB_MCP_TOOLSETS_ENV_VAR)
github_dynamic_toolsets = os.environ.get(GITHUB_MCP_DYNAMIC_TOOLSETS_ENV_VAR)
github_host = os.environ.get(GITHUB_HOST_ENV_VAR)

if not github_pat:
    print(f"Warning: The environment variable {GITHUB_PAT_ENV_VAR} is not set. The GitHub MCP Server will not be able to authenticate.")
    # Consider raising an error if strict configuration is required:
    # raise ValueError(f"Mandatory environment variable {GITHUB_PAT_ENV_VAR} is not set.")

# Prepare environment variables for the Docker container
docker_env_vars = {}
if github_pat: # Only pass PAT if it's set, though server will fail without it
    docker_env_vars[GITHUB_PAT_ENV_VAR] = github_pat
if github_toolsets:
    docker_env_vars[GITHUB_MCP_TOOLSETS_ENV_VAR] = github_toolsets
if github_dynamic_toolsets:
    docker_env_vars[GITHUB_MCP_DYNAMIC_TOOLSETS_ENV_VAR] = github_dynamic_toolsets
if github_host:
    docker_env_vars[GITHUB_HOST_ENV_VAR] = github_host

# Define the MCPToolset for the GitHub MCP Server
# The command arguments are set up to pass environment variables to the docker container.
# Note: Docker requires environment variables to be explicitly passed with `-e VAR_NAME=value`
# or just `-e VAR_NAME` if the value is to be inherited from the calling environment.
# For clarity and control, we are explicitly setting them in the `env` param of StdioServerParameters,
# which then passes them to the subprocess environment.
github_mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i", # Enables interactive mode, crucial for stdio communication
            "--rm", # Automatically remove the container when it exits
            # Pass environment variables to the Docker container.
            # Docker will use the values from the `env` dict provided below.
            "-e", GITHUB_PAT_ENV_VAR, # Essential for server operation
            "-e", GITHUB_MCP_TOOLSETS_ENV_VAR,
            "-e", GITHUB_MCP_DYNAMIC_TOOLSETS_ENV_VAR,
            "-e", GITHUB_HOST_ENV_VAR,
            "ghcr.io/github/github-mcp-server" # The official GitHub MCP server image
        ],
        env=docker_env_vars, # Pass the prepared environment variables to the subprocess
    )
    # Optional: tool_filter can be used here if you want to statically limit tools
    # tool_filter=['tool_name_1', 'tool_name_2']
)

# Create the LlmAgent instance
root_agent = LlmAgent(
    name="github_mcp_agent",
    model=LiteLlm(model=POWERFUL_MODEL),
    description="Agent to perform GitHub operations by connecting to the official GitHub MCP server using Docker. Requires a GitHub Personal Access Token.",
    instruction=(
        "You are an agent that interacts with GitHub via the official GitHub MCP server. "
        "Your environment MUST be configured with a GITHUB_PERSONAL_ACCESS_TOKEN for the server to work. "
        "Use the available tools, which are dynamically provided by the GitHub MCP server, to manage "
        "repositories, issues, users, pull requests, and other GitHub entities based on user requests. "
        "The GitHub MCP server can also be configured with optional environment variables: "
        "GITHUB_TOOLSETS (to specify enabled toolsets like 'repos,issues'), "
        "GITHUB_DYNAMIC_TOOLSETS (set to '1' for dynamic tool discovery), and "
        "GITHUB_HOST (for GitHub Enterprise Server users, e.g., 'https://github.example.com')."
    ),
    tools=[github_mcp_toolset],
)

# Example of how to potentially access the dynamically loaded tools (for debugging or logging)
# This part is optional and depends on how ADK handles tools post-initialization.
# It might require the agent to be run or initialized in some way first.
# print("Attempting to list tools from MCPToolset after agent potential initialization:")
# try:
#     if hasattr(github_mcp_toolset, '_tools') and github_mcp_toolset._tools:
#         for tool_name, tool_instance in github_mcp_toolset._tools.items():
#             print(f"Discovered tool: {tool_name} - {tool_instance.description}")
#     elif hasattr(github_mcp_toolset, 'tools') and github_mcp_toolset.tools: # ADK might change internal access
#          for tool_instance in github_mcp_toolset.tools: # Assuming tools is a list
#             print(f"Discovered tool: {tool_instance.name} - {tool_instance.description}")
#     else:
#         print("MCPToolset does not have a readily accessible list of discovered tools before full runtime initialization.")
# except Exception as e:
#     print(f"Could not list tools from MCPToolset: {e}")
