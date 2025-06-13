import requests
from .base_provider import AIBaseProvider

class ClaudeProvider(AIBaseProvider):
    """
    Provider implementation for Anthropic Claude.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        # The Claude API URL will be added here
        self.api_url = "https://api.anthropic.com/v1/messages" 

    def get_suggestion(self, prompt: str, context: str) -> str:
        """
        Queries the Claude API to get a command suggestion.
        
        NOTE: This is a mock implementation for now.
        """
        full_prompt = self._prepare_prompt(prompt, context)
        
        # API call logic (mocked for now)
        print(f"--- Sending to Claude ---")
        print(full_prompt)
        print("-----------------------")

        # Simulate an API response
        return "ls -la # Mock response from Claude" 