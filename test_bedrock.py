import os
import litellm
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file.
    # This will load AWS_PROFILE (and AWS_DEFAULT_REGION if present)
    # directly into os.environ.
    # By default, load_dotenv() does NOT override existing environment variables.
    # If you want the .env file to always take precedence, use load_dotenv(override=True)
    loaded_env = load_dotenv(override=True)

    if loaded_env:
        print("Loaded .env file. Variables from .env will override existing ones if any conflict.")
    else:
        print("Warning: .env file not found. Relying on pre-existing environment variables if any.")

    # Get the AWS_PROFILE value that is now in the environment.
    # boto3 (used by litellm) will automatically pick up AWS_PROFILE from os.environ.
    aws_profile_in_use = os.getenv("AWS_PROFILE")
    aws_region_in_use = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION")


    if not aws_profile_in_use:
        print("Error: AWS_PROFILE is not set in your environment or .env file.")
        print("Please ensure your .env file contains: AWS_PROFILE=\"your-profile-name\"")
        print("Or that AWS_PROFILE is exported in your shell environment.")
        return

    print(f"Using AWS Profile: {aws_profile_in_use}")
    if aws_region_in_use:
        print(f"Using AWS Region: {aws_region_in_use}")
        # Ensure AWS_REGION is also set as some tools might prefer it, though
        # AWS_DEFAULT_REGION is standard for boto3 configuration.
        os.environ["AWS_REGION"] = aws_region_in_use # Redundant if AWS_DEFAULT_REGION is picked up, but safe.
    else:
        print("Warning: AWS region (AWS_DEFAULT_REGION or AWS_REGION) is not set. ")
        print("Ensure your AWS profile specifies a default region, or set it in the .env file.")


    # Define the Bedrock model you want to test with
    # Replace with a model ID you have access to in your Bedrock region.
    bedrock_model = "bedrock/anthropic.claude-3-haiku-20240307-v1:0" # Example

    print(f"Attempting to call Bedrock model: {bedrock_model}")

    messages = [
        {"role": "user", "content": "Hello, Bedrock! Briefly introduce yourself."}
    ]

    try:
        response = litellm.completion(
            model=bedrock_model,
            messages=messages
        )
        print("\nBedrock Model Response:")
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            print(response.choices[0].message.content)
        else:
            print("Received an unexpected response structure:")
            print(response)

        print(f"\nSuccessfully authenticated and received response from Bedrock using profile: {aws_profile_in_use}")

    except Exception as e:
        print(f"\nAn error occurred:")
        print(e)
        print("\nPlease double-check the following:")
        print(f"1. The AWS profile '{aws_profile_in_use}' is correctly configured in your ~/.aws/credentials and ~/.aws/config files.")
        print(f"2. The profile '{aws_profile_in_use}' has the necessary IAM permissions for Amazon Bedrock and the model '{bedrock_model}'.")
        print(f"3. The model '{bedrock_model}' is available in the AWS region being used.")
        print("4. Your AWS credentials (if using static keys in the profile) are valid and not expired.")
        print("5. If your profile uses MFA, ensure you have an active MFA session for the AWS CLI if it relies on that, or that your profile handles MFA for SDK access.")

if __name__ == "__main__":
    main()