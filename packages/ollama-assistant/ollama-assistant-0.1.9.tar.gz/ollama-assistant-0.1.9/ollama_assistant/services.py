from ollama_assistant.models import Thread, Message
from mongoengine import DoesNotExist


class ThreadService:
    @staticmethod
    def create_thread(thread_id):
        thread = Thread(thread_id=thread_id)
        thread.save()
        return thread

    @staticmethod
    def delete_thread(thread_id):
        try:
            thread = Thread.objects.get(thread_id=thread_id)
            thread.delete()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def append_message(thread_id, role, content):
        try:
            thread = Thread.objects.get(thread_id=thread_id)
            message = Message(role=role, content=content)
            thread.messages.append(message)
            thread.save()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def fetch_thread(thread_id):
        try:
            return Thread.objects.get(thread_id=thread_id)
        except DoesNotExist:
            return None
