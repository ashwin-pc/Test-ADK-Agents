# GitHub MCP Agent

This agent interacts with GitHub using the official GitHub MCP Server (ghcr.io/github/github-mcp-server).
It allows performing various GitHub operations by connecting to this server, which runs in Docker.

## Prerequisites

- Docker installed and running.
- A GitHub Personal Access Token (PAT).

## Configuration

The agent requires the following environment variable to be set:

- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub PAT. This is mandatory for the GitHub MCP server to authenticate.

Optional environment variables to configure the GitHub MCP server:

- `GITHUB_TOOLSETS`: A comma-separated list of toolsets to enable (e.g., "repos,issues"). Available toolsets include `repos`, `issues`, `users`, `pull_requests`, `code_security`, `experiments`. If not set, the server defaults to all toolsets.
- `GITHUB_DYNAMIC_TOOLSETS`: Set to `1` to enable dynamic tool discovery by the MCP server (beta feature).
- `GITHUB_HOST`: If using GitHub Enterprise Server, set this to your GHES hostname (e.g., `https://github.example.com`).

Refer to the [official GitHub MCP Server documentation](https://github.com/github/github-mcp-server) for more details on server configuration.
