import os
from dotenv import load_dotenv
import litellm

# Ensure environment variables are loaded
load_dotenv()

class LLMConnector:
    """
    A class to abstract the connection to various LLM providers using LiteLLM.
    Supported providers: openai, groq, openrouter, deepseek, claudeai.
    """

    def __init__(self, provider: str, model: str, api_key: str = None, **kwargs):
        """
        Initializes the connector.
        
        Args:
            provider (str): The provider name (e.g., 'openai', 'groq', etc.).
            model (str): The model to use for the selected provider.
            api_key (str, optional): The API key for the provider. If not provided,
                                     it will be loaded from the environment variable 
                                     '{PROVIDER}_API_KEY'.
            **kwargs: Additional configuration parameters for LiteLLM.
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key if api_key else os.getenv(f"{provider.upper()}_API_KEY")
        if not self.api_key:
            raise ValueError(f"API key for provider '{provider}' is not provided or set in the environment.")
        self.config = kwargs

    def complete(self, prompt: str, temperature: float = 0.7, max_tokens: int = 150) -> str:
        """
        Sends the prompt to the LLM and returns the generated text.

        Args:
            prompt (str): The prompt to send.
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum number of tokens in the completion.

        Returns:
            str: The generated text.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        # Build parameters for the completion call.
        params = {
            "api_key": self.api_key,
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **self.config
        }
        # For Groq, do not include the "provider" parameter.
        if self.provider != "groq":
            params["provider"] = self.provider

        response = litellm.completion(**params)
        # Assuming the response follows an OpenAI-like format:
        return response["choices"][0]["message"]["content"].strip()