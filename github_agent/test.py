import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure the agent can be imported
# Add the parent directory to sys.path to allow importing from github_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGitHubMCPAgent(unittest.TestCase):

    @patch.dict(os.environ, {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "test_pat_value",
        "AGENT_POWERFUL_MODEL": "testing/dummy-model" # Ensure agent_models uses a test model
    })
    @patch('google.adk.tools.mcp_tool.mcp_toolset.MCPToolset.__init__')
    def test_agent_instantiation(self, mock_mcp_toolset_init):
        """Test that the GitHub MCP agent can be instantiated."""
        # Mock MCPToolset.__init__ to prevent it from trying to connect to Docker/npx
        # and to avoid errors if Docker isn't running or configured during tests.
        mock_mcp_toolset_init.return_value = None # MCPToolset.__init__ doesn't return anything

        # Mock the MCPToolset instance that will be created
        mock_toolset_instance = MagicMock()
        mock_toolset_instance.name = "mock_github_mcp_toolset"
        mock_toolset_instance.description = "A mock toolset for testing"
        mock_toolset_instance.get_tools = MagicMock(return_value={}) # Or return a list of mock tools
        
        # If MCPToolset is directly instantiated and passed,
        # we might need to patch where it's instantiated or how it's used.
        # For now, patching __init__ should prevent connection attempts.

        try:
            from github_agent import agent
            # Check if root_agent is an LlmAgent instance
            self.assertTrue(hasattr(agent, 'root_agent'), "agent.py does not define root_agent")
            self.assertIsNotNone(agent.root_agent, "root_agent is None")
            
            # Further check its properties if needed
            self.assertEqual(agent.root_agent.name, "github_mcp_agent")
            self.assertIn("GITHUB_PERSONAL_ACCESS_TOKEN", agent.root_agent.instruction)

            # Check if the mocked MCPToolset was called (it should be, during agent init)
            mock_mcp_toolset_init.assert_called_once()
            
            # Example: check arguments passed to MCPToolset constructor
            args, kwargs = mock_mcp_toolset_init.call_args
            self.assertIn('connection_params', kwargs)
            connection_params = kwargs['connection_params']
            self.assertEqual(connection_params.command, "docker")
            self.assertIn("ghcr.io/github/github-mcp-server", connection_params.args)
            self.assertIn("GITHUB_PERSONAL_ACCESS_TOKEN", connection_params.env)
            self.assertEqual(connection_params.env["GITHUB_PERSONAL_ACCESS_TOKEN"], "test_pat_value")

        except ImportError:
            self.fail("Failed to import github_agent.agent")
        except Exception as e:
            self.fail(f"Agent instantiation failed with an unexpected error: {e}")

if __name__ == '__main__':
    unittest.main()
