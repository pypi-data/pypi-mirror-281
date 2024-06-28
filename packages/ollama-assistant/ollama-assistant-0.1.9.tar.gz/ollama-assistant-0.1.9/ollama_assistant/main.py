from client import OllamaClient

ollama = OllamaClient(model='survey-model:latest')

thread = ollama.assistant.thread

print(thread.messages)

ollama.assistant.thread.messages.create_thread_message(
    thread_id = 'thread_6f93cfad-1c6d-4dfc-b1da-d77b8725a13d',
    role = 'user',
    content = "I don't know it's something the organization should figure out"
)

ollama.assistant.thread.run(thread_id='thread_6f93cfad-1c6d-4dfc-b1da-d77b8725a13d')

ollama.assistant.thread.messages.list_messages(thread_id='thread_6f93cfad-1c6d-4dfc-b1da-d77b8725a13d')