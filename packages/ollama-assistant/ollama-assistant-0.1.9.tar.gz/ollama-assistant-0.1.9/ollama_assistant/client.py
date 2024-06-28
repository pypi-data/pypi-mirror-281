import logging
from mongoengine import connect
from ollama_assistant.settings import (
    DEFAULT_API_URL,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)
from ollama_assistant.chat import Chat
from ollama_assistant.assistant import Assistant


class OllamaClient:
    """
    OllamaClient provides a high-level interface to interact with Ollama services.

    Parameters
    ----------
    api_url : str, optional
        Base URL for the API endpoints.
    model : str, optional
        The model used by the generation and chat services, default is 'mistrel'.
    db_host : str, optional
        Database host address, default is 'localhost'.
    db_port : int, optional
        Database port number, default is 27017.
    db_name : str, optional
        Database name, default is 'ollama_db'.
    """

    def __init__(
        self,
        api_url=None,
        model=None,
        db_host=None,
        db_port=None,
        db_name=None,
        db_user=None,
        db_password=None,
    ):
        self.__base_url = api_url or DEFAULT_API_URL
        self.__connect_to_db(
            db_host=db_host or DB_HOST,
            db_port=db_port or DB_PORT,
            db_name=db_name or DB_NAME,
            db_user=db_user or DB_USER,
            db_password=db_password or DB_PASSWORD,
        )
        self.__assistant = Assistant(model=model or "mistrel", api_url=self.__base_url)

    def __connect_to_db(self, db_host, db_port, db_name, db_user, db_password):
        try:
            if db_user and db_password:
                connection_string = (
                    f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                )
            else:
                connection_string = f"mongodb://{db_host}:{db_port}/{db_name}"

            connect(db_name, host=connection_string)
            logging.info(f"Connected to MongoDB at {connection_string}")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise

    @property
    def assistant(self):
        """Provides access to the assistant thread."""
        return self.__assistant
