import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class SerperDevTool:
    """
    A tool to interact with the Serper API for internet search.
    
    Example Usage:
        from utils.serper_dev_tool import SerperDevTool
        serper = SerperDevTool()
        results = serper.search("best practices for semantic search")
        for result in results.get("items", []):
            print(result["title"], result["link"])
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key if api_key else os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY is not set in the .env file.")
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }
        payload = {
            "q": query,
            "gl": "US",
            "hl": "en-US"
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error in Serper request: {response.status_code} - {response.text}")
            return {}