import json
import requests
import logging
from ollama_assistant.settings import DEFAULT_API_URL

# Assuming 'settings.py' contains DEFAULT_API_URL and possibly other settings


class Chat:
    def __init__(
        self, model: str = "mistrel", api_url: str = None, stream: bool = False
    ):
        self.__base_url = api_url or DEFAULT_API_URL
        self.__model = model
        self.__stream = stream
        self.__headers = {"Content-Type": "application/json"}

    def chat(self, messages: list, output_format: str = "") -> str:
        """
        Send messages to the chat endpoint and get a response.

        Parameters
        ----------
        messages : list
            A list of message dicts to send to the server.

        Returns
        -------
        str
            The response message from the server, or an empty string if an error occurs.
        """
        url = f"{self.__base_url}/chat"
        data = {
            "model": self.__model,
            "stream": self.__stream,
            "messages": messages,
        }

        if output_format:
            data["format"] = output_format

        try:
            response = requests.post(url, headers=self.__headers, data=json.dumps(data))
            response.raise_for_status()
            response_data = response.json()
            actual_response = response_data.get("message", "")
            return actual_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during chat: {e}")
            return None


# Be sure to initialize the logging system at the start of your application
# logging.basicConfig(level=logging.INFO)

# Example usage:
# chat = Chat(model='gpt3', api_url='http://api.example.com', stream=True)
# response = chat.chat(messages=[{"role": "user", "content": "Hello!"}])
# if response:
#     print(response)
