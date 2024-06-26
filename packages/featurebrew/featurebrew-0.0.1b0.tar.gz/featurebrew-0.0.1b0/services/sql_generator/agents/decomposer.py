from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from sql_generator.agents.base import BaseAgent
from sql_generator.const import *
from sql_generator.tools.llm import safe_call_llm
from sql_generator.utils import *
from typing import List
from copy import deepcopy

import sqlite3
import time
import abc
import sys
import os
import glob
import pandas as pd
from tqdm import tqdm, trange
from pprint import pprint
import pdb
import tiktoken

# DATA_CHROMA_PATH = os.getenv("DATA_DB_PATH")
# DATA_COLLECTION = os.getenv("DATA_DB_COLLECTION")

PLATFORM_QA_MODEL = os.getenv("PLATFORM_QA_MODEL", "gpt-4o")

data_path="/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/data"


class Decomposer(BaseAgent):
    """
    Decompose the question and solve them using CoT
    """
    name = DECOMPOSER_NAME
    description = "Decompose the question and solve them using CoT"

    def __init__(self):
        super().__init__()
        self._message = {}

    def talk(self, message: dict):
        """
        :param self:
        :param message: {"query": user_query,
                        "evidence": extra_info,
                        "desc_str": description of db schema,
                        "fk_str": foreign keys of database}
        :return: decompose question into sub ones and solve them in generated SQL
        """
        if message['send_to'] != self.name: return
        self._message = message
        query, evidence, schema_info, fk_info = message.get('query'), \
            message.get('evidence'), \
            message.get('desc_str'), \
            message.get('fk_str')

        decompose_template = decompose_template_spider
        prompt = decompose_template.format(query=query, desc_str=schema_info, fk_str=fk_info)

        ## one shot decompose(first) # fixme
        # prompt = oneshot_template_2.format(query=query, evidence=evidence, desc_str=schema_info, fk_str=fk_info)
        word_info = extract_world_info(self._message)
        reply = safe_call_llm(prompt, **word_info).strip()

        res = ''
        qa_pairs = reply

        try:
            res = parse_sql_from_string(reply)
        except Exception as e:
            res = f'error: {str(e)}'
            print(res)
            time.sleep(1)

        ## Without decompose
        # prompt = zeroshot_template.format(query=query, evidence=evidence, desc_str=schema_info, fk_str=fk_info)
        # reply = LLM_API_FUC(prompt)
        # qa_pairs = []

        message['final_sql'] = res
        message['qa_pairs'] = qa_pairs
        message['fixed'] = False
        message['send_to'] = REFINER_NAME

        return message

    def invoke(self, message):
        # data_system_prompt = SystemMessagePromptTemplate(
        #     prompt=PromptTemplate(
        #         input_variables=["evidence", "desc_str", "fk_str"], template=selector_template
        #     )
        # )
        #
        # data_human_prompt = HumanMessagePromptTemplate(
        #     prompt=PromptTemplate(input_variables=["query"], template="{query}")
        # )
        # messages = [data_system_prompt, data_human_prompt]
        #
        # data_prompt = ChatPromptTemplate(
        #     input_variables=["evidence", "desc_str", "fk_str", "query"], messages=messages
        # )
        #
        # chat_model = ChatOpenAI(model=PLATFORM_QA_MODEL, temperature=0.0)

        response = self.talk(message)
        return response


def initialize_decomposer_agent():
    data_retriever = Decomposer()
    return data_retriever


if __name__ == "__main__":
    data_retriever = initialize_decomposer_agent()
    message = {}
    decomposer_data_chain = data_retriever.invoke(message, 'How many singers do we have?')
    print(decomposer_data_chain)
