import uuid
import logging
from ollama_assistant.messages import Messages
from ollama_assistant.chat import Chat


class AssistantThread:
    """
    AssistantThread manages the lifecycle of a chat thread and its messages.

    Parameters
    ----------
    model : str, optional
        The model used by the chat thread, default is 'mistrel'.
    """

    def __init__(self, api_url, model="mistrel"):
        self.__base_url = api_url
        self.__messages = Messages()
        self.__chat = Chat(model=model, api_url=self.__base_url)

    def __generate_thread_id(self) -> str:
        """
        Generates a unique thread ID.

        Returns
        -------
        str or None
            A unique thread ID string, or None if an error occurred during generation.
        """
        try:
            return f"thread_{uuid.uuid4()}"
        except Exception as e:
            logging.error(f"Error occurred during thread ID generation: {e}")
            return None

    def create(self):
        """
        Creates a new thread with a unique thread ID and initializes the message manager.

        Returns
        -------
        AssistantThread
            The instance of AssistantThread with a new thread created.
        """
        self.__thread_id = self.__generate_thread_id()
        self.__messages.init_thread_messages(thread_id=self.__thread_id)
        # other logic if required
        return self

    def run(self, thread_id=None, json_formatting=False):
        """
        Runs the chat thread by fetching messages and sending them to the chat service.
        """
        if not thread_id:
            logging.warning("Thread has not been created yet.")
            return

        thread_messages = self.__messages.list_messages(thread_id)

        output_format = "json" if json_formatting else ""

        response = self.__chat.chat(thread_messages, output_format)
        if response and "role" in response and "content" in response:
            self.__messages.create_thread_message(
                thread_id=thread_id,
                role=response["role"],
                content=response["content"],
            )
        else:
            logging.error("The chat response did not contain the necessary elements.")

    @property
    def id(self) -> str:
        """
        The thread_id property representing the ID of the current chat thread.

        Returns
        -------
        str
            The thread ID of the current chat thread.
        """
        return self.__thread_id

    @property
    def messages(self):
        """
        The messages property representing the message manager of the current chat thread.

        Returns
        -------
        Messages
            The message manager responsible for handling messages of the current chat thread.
        """
        return self.__messages


# Be sure to initialize the logging system at the start of your application
# logging.basicConfig(level=logging.INFO)

# Example usage:
# assistant_thread = AssistantThread(model='gpt3')
# assistant_thread.create()
# assistant_thread.run()
# print(assistant_thread.messages.list_messages(assistant_thread.thread_id))
