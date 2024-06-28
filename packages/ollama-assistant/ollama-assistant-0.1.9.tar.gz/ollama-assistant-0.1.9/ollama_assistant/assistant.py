from ollama_assistant.assistant_thread import AssistantThread


class Assistant:
    """
    The Assistant class represents an entity capable of managing an assistant thread
    for processing chat messages based on the given model.

    Parameters
    ----------
    model : str, optional
        The name of the model used by the assistant, by default 'mistrel'.

    Attributes
    ----------
    __thread : AssistantThread
        An instance of AssistantThread which handles message threading.
    """

    def __init__(self, api_url, model="mistrel"):
        """
        Initialize an Assistant with a specified model.
        """
        self.__base_url = api_url
        self.__thread = AssistantThread(model=model,api_url=self.__base_url)

    @property
    def thread(self):
        """
        The thread property gives access to the Assistant's thread handle.

        Returns
        -------
        AssistantThread
            Returns the instance of AssistantThread associated with this Assistant.
        """
        return self.__thread


# Assuming `assistant_thread.py` is another module that contains the AssistantThread class
# Example usage:
# assistant = Assistant(model='gpt3')
# assistant_thread = assistant.thread
# Do something with assistant_thread
