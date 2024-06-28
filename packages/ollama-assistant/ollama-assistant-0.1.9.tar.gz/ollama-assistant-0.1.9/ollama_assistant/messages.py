import logging
from ollama_assistant.services import ThreadService


class Messages:
    def __init__(self):
        """
        Initialize the Messages service instance.
        """
        self.__thread_service = ThreadService()

    def init_thread_messages(self, thread_id: str):
        thread = self.__thread_service.fetch_thread(thread_id)
        if not thread:
            logging.info(
                f"Thread with id {thread_id} does not exist, creating a new one."
            )
            self.__thread_service.create_thread(thread_id=thread_id)

    def create_thread_message(self, thread_id: str, role: str = "", content: str = ""):
        """
        Create a message in the specified thread.

        Parameters
        ----------
        thread_id : str
            The identifier of the thread.
        role : str
            The role of the message sender (e.g., 'user', 'assistant').
        content : str
            The message content.

        Notes
        -----
        If the thread does not exist, it will be created.
        """

        thread = self.__thread_service.fetch_thread(thread_id)
        if not thread:
            logging.info(f"Thread with id {thread_id} does not exist")
            raise ValueError(f"Thread with id {thread_id} does not exist")

        self.__thread_service.append_message(
            thread_id=thread_id, role=role, content=content
        )

    def list_messages(self, thread_id: str):
        """
        List all messages from the specified thread.

        Parameters
        ----------
        thread_id : str
            The identifier of the thread to list messages from.

        Returns
        -------
        list of dict
            A list of dictionaries containing the 'role' and 'content' of each message.
        """
        thread = self.__thread_service.fetch_thread(thread_id)
        if thread:
            return [
                {"role": message.role, "content": message.content}
                for message in thread.messages
            ]
        else:
            logging.error(f"Thread with id {thread_id} does not exist")
            raise ValueError(f"Thread with id {thread_id} does not exist")
