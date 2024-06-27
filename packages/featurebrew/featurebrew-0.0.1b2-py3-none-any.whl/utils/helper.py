import asyncio
from datetime import datetime

import docx
import dotenv
import logging
import os
import gzip
import shutil
import sys
import tempfile
from typing import Any
from urllib.parse import urlparse

import docx
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import WebBaseLoader, UnstructuredMarkdownLoader, UnstructuredHTMLLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.xml import UnstructuredXMLLoader
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_openai_functions_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
)


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str, multi: bool = False):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    if multi:
        prompt = hub.pull("hwchase17/openai-functions-agent")
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools,
                             return_intermediate_steps=True,
                             verbose=True,
                             early_stopping_method="generate",
                             max_iterations=100
                             )
    return executor


def agent_content_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result.content, name=name)]}


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


# Either agent can decide to end
def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        # The previus agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "end"
    return "continue"


def DocxLoader(file_path):
    # Load the .docx file
    doc = docx.Document(file_path)

    # Extract text from each paragraph in the document
    text = [paragraph.text for paragraph in doc.paragraphs]

    # Combine the text into a single string, separating paragraphs with newlines
    combined_text = '\n'.join(text)

    return combined_text

# Function to check if the given path is a URL
def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Example of loading and using document loaders
def load_document(file_path: str, loader_class: Any) -> Any:
    """Download a document from a URL, save it, and load it using a specified loader class.

    Args:
        file_path: File path of the downloaded document.
        loader_class: The class of loader to use for loading the document.

    Returns:
        The loaded document.
    """
    loader = loader_class(file_path=file_path)
    return loader.load()

def doc_loader(file_path: str, file_extension: str) -> Any:
    if is_url(file_path):
        document = load_document(file_path, UnstructuredHTMLLoader)  # Use WebBaseLoader for URLs
    elif file_extension and file_extension == ".csv":
        document = load_document(file_path, CSVLoader)
    elif file_extension and file_extension == ".pdf":
        document = load_document(file_path, PyPDFLoader)
    elif file_extension and file_extension == ".xml":
        document = load_document(file_path, UnstructuredXMLLoader)
    elif file_extension and file_extension == ".docx":
        document = load_document(file_path, DocxLoader)
    elif file_extension and file_extension == ".json":
        document = load_document(file_path, JSONLoader)
    elif file_extension and file_extension == ".md":
        document = load_document(file_path, UnstructuredMarkdownLoader)
    elif file_extension and file_extension == ".gz":
        # Create a temporary directory
        tmp_dir = tempfile.mkdtemp()

        # Construct the path for the uncompressed file
        # This assumes the original file has a '.gz' extension and strips it for the uncompressed filename
        uncompressed_file_path = os.path.join(tmp_dir, os.path.basename(file_path).removesuffix('.gz'))

        # Open the .gz file and uncompress it
        with gzip.open(file_path, 'rb') as gz_file:
            with open(uncompressed_file_path, 'wb') as uncompressed_file:
                shutil.copyfileobj(gz_file, uncompressed_file)
        document = load_document(uncompressed_file_path, TextLoader)
    else:
        document = load_document(file_path, TextLoader)

    return document
