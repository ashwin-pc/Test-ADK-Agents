import os
import subprocess
import json
from typing import Optional, Dict, List, Any, Union
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import sys
import shlex
import shutil

# Add the parent directory to sys.path to allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_models import POWERFUL_MODEL

# Use zsh as the shell if it's available, fallback to bash
SHELL = '/bin/zsh' if os.path.exists('/bin/zsh') else '/bin/bash'

CLAUDE_CODE_CMD = os.getenv("CLAUDE_CODE_CMD", "claude")

def execute_claude_code(prompt: str, repo_path: str) -> dict:
    """
    Execute a Claude Code command on a repository.
    
    Args:
        prompt (str): The instruction or query for Claude Code
        repo_path (str): The path to the repository to analyze
        
    Returns:
        dict: Status and result or error message
    """
    try:
        # Verify that Claude Code CLI is installed and available
        try:
            # Use a single shell command for compatibility with aliases
            version_cmd = f"{CLAUDE_CODE_CMD} --version"
            version_output = subprocess.check_output(
                version_cmd,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,
                executable=SHELL  # Use zsh or fallback to bash
            )
            # Extract version information to include in the result
            version_info = version_output.strip()
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "error_message": f"{CLAUDE_CODE_CMD} CLI is not installed or not in PATH. Error: {str(e)}"
            }
        
        # Verify the repository path exists
        if not os.path.isdir(repo_path):
            return {
                "status": "error",
                "error_message": f"Repository path does not exist: {repo_path}"
            }
            
        # Change to the repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        try:
            # Execute Claude Code with the given prompt
            # Create command with proper escaping for shell
            prompt_escaped = shlex.quote(prompt)
            cmd = f"{CLAUDE_CODE_CMD} -p {prompt_escaped}"
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                executable=SHELL  # Use zsh or fallback to bash
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                return {
                    "status": "error",
                    "error_message": f"Claude Code execution failed: {stderr}",
                    "exit_code": process.returncode
                }
            
            # Parse the JSON response
            try:
                response_data = json.loads(stdout)
                return {
                    "status": "success",
                    "result": response_data,
                    "claude_version": version_info
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw output
                return {
                    "status": "success",
                    "result": stdout,
                    "claude_version": version_info
                }
                
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to execute Claude Code: {str(e)}"
        }

def search_repository(query: str, repo_path: str, file_patterns: Optional[List[str]] = None) -> dict:
    """
    Search for code, patterns or concepts in a repository using Claude Code.
    
    Args:
        query (str): The search query
        repo_path (str): The path to the repository to analyze
        file_patterns (Optional[List[str]]): Optional list of file patterns to include in search
        
    Returns:
        dict: Status and search results or error message
    """
    try:
        pattern_arg = ""
        if file_patterns:
            patterns = ",".join(file_patterns)
            pattern_arg = f" --include=\"{patterns}\""
            
        # Construct search prompt - use explicit quotes to handle spaces in query
        query_escaped = query.replace('"', '\\"')  # Escape double quotes in query
        prompt = f'search{pattern_arg} "{query_escaped}"'
        
        return execute_claude_code(prompt, repo_path)
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Repository search failed: {str(e)}"
        }

def explain_code(file_path: str, repo_path: str, line_range: Optional[str] = None) -> dict:
    """
    Explain code in a file using Claude Code.
    
    Args:
        file_path (str): The path to the file to explain, relative to repo_path
        repo_path (str): The path to the repository
        line_range (Optional[str]): Optional line range to explain (e.g. "10-20")
        
    Returns:
        dict: Status and explanation or error message
    """
    try:
        # Build the file path - handle absolute and relative paths
        if os.path.isabs(file_path):
            # Convert to relative path if it's within repo_path
            abs_repo_path = os.path.abspath(repo_path)
            if file_path.startswith(abs_repo_path):
                file_path = os.path.relpath(file_path, abs_repo_path)
            else:
                return {
                    "status": "error",
                    "error_message": f"File path {file_path} is not within repository {repo_path}"
                }
        
        # Construct line range argument if specified
        line_arg = ""
        if line_range:
            line_arg = f":{line_range}"
            
        # Construct explain prompt
        prompt = f"explain {file_path}{line_arg}"
        
        return execute_claude_code(prompt, repo_path)
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Code explanation failed: {str(e)}"
        }

def modify_code(instruction: str, file_path: str, repo_path: str) -> dict:
    """
    Modify code in a file using Claude Code.
    
    Args:
        instruction (str): The instruction for how to modify the code
        file_path (str): The path to the file to modify, relative to repo_path
        repo_path (str): The path to the repository
        
    Returns:
        dict: Status and result or error message
    """
    try:
        # Build the file path - handle absolute and relative paths
        if os.path.isabs(file_path):
            # Convert to relative path if it's within repo_path
            abs_repo_path = os.path.abspath(repo_path)
            if file_path.startswith(abs_repo_path):
                file_path = os.path.relpath(file_path, abs_repo_path)
            else:
                return {
                    "status": "error",
                    "error_message": f"File path {file_path} is not within repository {repo_path}"
                }
        
        # Construct modify prompt
        # Format is: edit [file_path] "[instruction]"
        instruction_escaped = instruction.replace('"', '\\"')  # Escape double quotes 
        prompt = f'edit {file_path} "{instruction_escaped}"'
        
        return execute_claude_code(prompt, repo_path)
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Code modification failed: {str(e)}"
        }

def execute_task(task: str, repo_path: str) -> dict:
    """
    Execute a general task in the repository using Claude Code.
    
    Args:
        task (str): The task to execute
        repo_path (str): The path to the repository
        
    Returns:
        dict: Status and result or error message
    """
    try:
        # For general tasks, just pass the task directly to Claude Code
        return execute_claude_code(task, repo_path)
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Task execution failed: {str(e)}"
        }

# Create the Repository agent with Claude Code
repo_agent = LlmAgent(
    name="repo_agent",
    model=LiteLlm(model=POWERFUL_MODEL),
    description="Agent to interact with code repositories using Claude Code",
    instruction=(
        "You are a helpful agent who can analyze, explain, and modify code in repositories "
        "using Claude Code as a tool. You can search for patterns, explain code functionality, "
        "modify existing code, and execute general tasks within a repository. Be precise and "
        "informative when explaining search results or code changes."
    ),
    tools=[
        search_repository,
        explain_code,
        modify_code,
        execute_task,
    ],
)

# Export the agent
root_agent = repo_agent