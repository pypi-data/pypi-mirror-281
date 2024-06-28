# setup.py
from setuptools import setup, find_packages

setup(
    name="ollama-assistant",
    version="0.1.9",
    description="A Python client library for implementing open ai like assistant feature with the Ollama services.",
    author="Glen",
    author_email="glenprojects666@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "mongoengine",
        "python-dotenv",
        # add other dependencies as needed
    ],
)
