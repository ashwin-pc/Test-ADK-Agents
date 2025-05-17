import os
import litellm
from dotenv import load_dotenv
from agent_models import FAST_MODEL

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


def main():
    print_header("AWS Bedrock Connection Test")
    
    # Load environment variables from .env file
    print_section("Environment Setup")
    loaded_env = load_dotenv(override=True)

    if loaded_env:
        print_success("Loaded .env file successfully")
    else:
        print_warning(".env file not found. Using existing environment variables")

    # Get AWS configuration
    aws_profile_in_use = os.getenv("AWS_PROFILE")
    aws_region_in_use = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION")

    if not aws_profile_in_use:
        print_error("AWS_PROFILE is not set in your environment or .env file")
        print_info("Please ensure your .env file contains: AWS_PROFILE=\"your-profile-name\"")
        print_info("Or that AWS_PROFILE is exported in your shell environment")
        return

    print_section("AWS Configuration")
    print_info(f"AWS Profile: {Colors.BOLD}{aws_profile_in_use}{Colors.END}{Colors.CYAN}")
    
    if aws_region_in_use:
        print_info(f"AWS Region: {Colors.BOLD}{aws_region_in_use}{Colors.END}{Colors.CYAN}")
        os.environ["AWS_REGION"] = aws_region_in_use
    else:
        print_warning("AWS region (AWS_DEFAULT_REGION or AWS_REGION) is not set")
        print_info("Ensure your AWS profile specifies a default region, or set it in the .env file")

    # Use the predefined fast model
    bedrock_model = FAST_MODEL
    
    print_section("Bedrock API Test")
    print_info(f"Testing model: {Colors.BOLD}{bedrock_model}{Colors.END}{Colors.CYAN}")

    messages = [
        {"role": "user", "content": "Hello, Bedrock! Briefly introduce yourself."}
    ]

    try:
        response = litellm.completion(
            model=bedrock_model,
            messages=messages
        )
        
        print_section("Bedrock Response")
        
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            content = response.choices[0].message.content.strip()
            print_info(content)
        else:
            print_warning("Received an unexpected response structure:")
            print(response)

        print_section("Test Results")
        print_success(f"Successfully connected to AWS Bedrock using profile: {aws_profile_in_use}")
        print_success("API request completed successfully")
        print_success("Model response received correctly")

    except Exception as e:
        print_section("Error Information")
        print_error(f"An error occurred: {str(e)}")
        
        print_section("Troubleshooting")
        print_info(f"1. Check that AWS profile '{aws_profile_in_use}' is correctly configured")
        print_info(f"2. Verify that profile has necessary IAM permissions for Bedrock and model '{bedrock_model}'")
        print_info(f"3. Confirm model '{bedrock_model}' is available in region '{aws_region_in_use}'")
        print_info("4. Check that AWS credentials are valid and not expired")
        print_info("5. If using MFA, ensure you have an active session")


if __name__ == "__main__":
    main()