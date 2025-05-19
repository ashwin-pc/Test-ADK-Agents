# Weather & Time Agent

This is a simple test agent that demonstrates core functionality by providing weather and time information for a specific city (currently only supports New York).

## Features

- **Get Weather**: Retrieve the current weather report for a city
- **Get Current Time**: Get the current time for a city, with proper timezone information

## Requirements

- Python with dependencies in `requirements.txt`
- AWS credentials for accessing Bedrock models

## Usage

```python
from test_agent.agent import root_agent

# Get weather information
result = root_agent.tools.get_weather(city="New York")
if result["status"] == "success":
    print(result["report"])
else:
    print(result["error_message"])

# Get current time
result = root_agent.tools.get_current_time(city="New York")
if result["status"] == "success":
    print(result["report"])
else:
    print(result["error_message"])
```

## Limitations

- Current implementation only supports New York City
- Weather data is currently mocked (not real-time data)
- Time data uses system clock with the appropriate timezone

## Testing

To test the agent's connection to AWS Bedrock, run:

```bash
python test.py
```

This test script will:
1. Verify your AWS configuration
2. Test the connection to the AWS Bedrock API
3. Confirm that the agent can successfully communicate with the chosen model

## Future Development

This agent serves primarily as a proof-of-concept for the LLM agent framework. Future versions may include:
- Support for multiple cities
- Integration with real weather API data
- Additional time and weather-related functions