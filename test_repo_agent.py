import os
from dotenv import load_dotenv
import subprocess
import sys
import argparse
import json
import shlex
import shutil

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}\n")

def print_section(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{message}{Colors.END}")
    print(f"{Colors.BLUE}{'-' * 40}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.CYAN}{message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

CLAUDE_CODE_CMD = os.getenv("CLAUDE_CODE_CMD", "claude")

def check_claude_code_installation():
    """Check if Claude Code CLI is installed and available in PATH."""
    print_section(f"Checking Claude Code Installation (command: {CLAUDE_CODE_CMD})")
    
    try:
        # Use a shell command to support aliases
        version_cmd = f"{CLAUDE_CODE_CMD} --version"
        version_output = subprocess.check_output(
            version_cmd, 
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            executable='/bin/zsh'  # Explicitly use zsh for alias support
        )
        print_success(f"Claude Code is installed: {version_output.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error executing {CLAUDE_CODE_CMD}: {e}")
        return False
    except FileNotFoundError:
        print_error(f"{CLAUDE_CODE_CMD} CLI not found in PATH")
        print_info("To install Claude Code, run: npm install -g @anthropic-ai/claude-code")
        print_info(f"To use a custom alias, set the CLAUDE_CODE_CMD environment variable to your alias (e.g., 'cc')")
        return False

def test_repository_access(repo_path):
    """Test access to the specified repository path."""
    print_section(f"Testing Repository Access")
    
    if not os.path.exists(repo_path):
        print_error(f"Repository path does not exist: {repo_path}")
        return False
        
    if not os.path.isdir(repo_path):
        print_error(f"Path exists but is not a directory: {repo_path}")
        return False
        
    # Check if it has .git directory (optional, but helpful)
    git_dir = os.path.join(repo_path, ".git")
    if os.path.isdir(git_dir):
        print_success(f"Path is a git repository: {repo_path}")
    else:
        print_warning(f"Path may not be a git repository (no .git directory found): {repo_path}")
        
    # Check if we can list files
    try:
        files = os.listdir(repo_path)
        print_success(f"Successfully listed {len(files)} files/directories in repository")
        return True
    except Exception as e:
        print_error(f"Error accessing repository contents: {str(e)}")
        return False

def test_claude_code_query(repo_path, query="list files"):
    """Test a simple Claude Code query on the repository."""
    print_section("Testing Claude Code Query")
    
    try:
        # Save current directory
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        try:
            print_info(f"Executing query: '{query}'")
            
            # Execute claude-code with the query using a shell command for alias compatibility
            query_escaped = shlex.quote(query)
            cmd = f"source ~/.zshrc && {CLAUDE_CODE_CMD} -p {query_escaped}"
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                executable='/bin/zsh'  # Use zsh for alias support
            )

            # Print the command for debugging
            print_info(f"Command: {cmd}")
            
            stdout, stderr = process.communicate()

            # Always print stdout and stderr for debugging
            print_info(f"STDOUT: {stdout if stdout.strip() else '(no content)'}")
            print_info(f"STDERR: {stderr if stderr.strip() else '(no content)'}")

            if process.returncode != 0:
                print_error(f"Claude Code query failed with exit code {process.returncode}")
                print_error(f"Error: {stderr}")
                return False

            # Try to parse as JSON
            try:
                result = json.loads(stdout)
                print_success("Query executed successfully")
                print_info("Response format: JSON")
                return True
            except json.JSONDecodeError:
                # If not JSON, just show raw output
                print_success("Query executed successfully")
                print_info("Response format: Text")
                if len(stdout) > 500:
                    print_info(f"Response preview: {stdout[:500]}...")
                else:
                    print_info(f"Response: {stdout}")
                return True
                
        finally:
            # Change back to original directory
            os.chdir(original_dir)
            
    except Exception as e:
        print_error(f"Error executing Claude Code query: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test the Repository Agent with Claude Code")
    parser.add_argument("--repo-path", required=True, help="Path to the repository to test with")
    parser.add_argument("--query", default="list files", help="Test query to run (default: 'list files')")
    args = parser.parse_args()
    
    print_header("Repository Agent Test")
    
    # Load environment variables from .env file
    print_section("Environment Setup")
    loaded_env = load_dotenv(override=True)
    
    if loaded_env:
        print_success("Loaded .env file successfully")
    else:
        print_warning(".env file not found. Using existing environment variables")
    
    # Repository path
    repo_path = os.path.expanduser(args.repo_path)
    print_info(f"Using repository path: {repo_path}")
    print_info(f"Current working directory: {os.getcwd()}")
    
    # Check Claude Code installation
    if not check_claude_code_installation():
        return
        
    # Check repository access
    if not test_repository_access(repo_path):
        return
        
    # Test Claude Code query
    if not test_claude_code_query(repo_path, args.query):
        return
    
    print_header("Repository Agent Test Complete")
    print_info("The repository agent is ready to use!")

if __name__ == "__main__":
    main()