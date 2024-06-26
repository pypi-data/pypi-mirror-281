import os

from services.sql_generator.const import di_selector_template, SELECTOR_NAME
from langchain_core.tools import tool, Tool
from services.sql_generator.agents.selector import initialize_selector_agent


@tool
def create_table_selector_agent(database_id, query):
    """Get the selector client response for passed database_id and query formatted as a string.
    This helps solve prediction (classification) query for users and returns the relevant tables
    in the dataset required as features for the passed query."""
    data_retriever = initialize_selector_agent(data_path="../../data/datasets/spider/database",
                                               tables_json_path="../../data/datasets/spider/tables.json",
                                               prompt_template=di_selector_template,
                                               lazy=True)
    message = {
            "db_id": database_id,
            "extracted_schema": {},
            "evidence": "",
            "query": query,
            "send_to": SELECTOR_NAME
        }
    # selector_data_chain = data_retriever.invoke(database_id, query)
    # print(selector_data_chain)
    return data_retriever.invoke(message)

tools = [create_table_selector_agent]
# tools = [create_table_selector_agent, repl_tool]

def get_di_agent_executor():
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model=os.getenv("MODEL"))

    from langgraph.prebuilt import create_react_agent
    ds_agent_executor = create_react_agent(model, tools)
    return ds_agent_executor