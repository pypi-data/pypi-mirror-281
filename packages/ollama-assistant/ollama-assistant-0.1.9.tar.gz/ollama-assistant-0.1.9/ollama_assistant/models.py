from mongoengine import Document, EmbeddedDocument, StringField, EmbeddedDocumentListField

class Message(EmbeddedDocument):
    role = StringField(required=True)
    content = StringField(required=True)

class Thread(Document):
    thread_id = StringField(required=True)
    messages = EmbeddedDocumentListField(Message)