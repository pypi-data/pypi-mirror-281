import os
import pandas as pd
import json

from langchain_experimental.utilities import PythonREPL
from langchain_experimental.tools import PythonREPLTool
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

from langchain_core.tools import tool, Tool

_DIVIDER = "\n\n---=======---\n\n"


@tool
def get_dataset_info(dataset_id: str) -> dict:
    """Get the dataset location for passed string dataset_id.
    Returns dictionary with dataset resources information."""
    storage_path = os.getenv('STORAGE_PATH')
    dataset_json_path = os.path.join(storage_path, "datasets", dataset_id, 'dataset.json')
    try:
        with open(dataset_json_path, 'r') as json_file:
            dataset_info = json.load(json_file)
        return dataset_info
    except FileNotFoundError:
        print(f"File not found: {dataset_json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {dataset_json_path}")
        return None


@tool
def get_dataset_processed_file_path(dataset_id: str) -> str:
    """Get the processed dataset file path for passed string dataset_id.
        Returns string path."""
    storage_path = os.getenv('STORAGE_PATH')
    processed_path = os.path.join(storage_path, "datasets", dataset_id, dataset_id + "-processed.csv")
    return processed_path


@tool
def get_dataset_features(dataset_id: str) -> dict:
    """Get the dataset recommended features for passed string dataset_id.
    Returns dictionary with dataset resources information."""
    storage_path = os.getenv('STORAGE_PATH')
    dataset_json_path = os.path.join(storage_path, "datasets", dataset_id, f'{dataset_id}-features.json')
    try:
        with open(dataset_json_path, 'r') as json_file:
            dataset_info = json.load(json_file)
        return dataset_info
    except FileNotFoundError:
        print(f"File not found: {dataset_json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {dataset_json_path}")
        return None


@tool
def get_dataset_schema(dataset_id: str) -> dict:
    """Get the dataset schema for passed string dataset_id.
    Returns relevant string with dataset schema information for user query."""
    storage_path = os.getenv('STORAGE_PATH')
    dataset_json_path = os.path.join(storage_path, "datasets", dataset_id, 'schema.json')
    try:
        with open(dataset_json_path, 'r') as file:
            dataset_info = file.read()
        return dataset_info
    except FileNotFoundError:
        print(f"File not found: {dataset_json_path}")
        return None


@tool
def persist_transformation_code(dataset_id: str, code_content: str, user_query: str):
    """
    Persists the transformation code to the local path.
    Pass params dataset_id, code_content, user_query.
    """
    storage_path = os.getenv('STORAGE_PATH')
    code_path = os.path.join(storage_path, "datasets", dataset_id, f'data_clean_{dataset_id}.py')
    try:
        with open(code_path, 'w') as file:
            file.write(f"# {user_query}")
            file.write(code_content)
    except FileNotFoundError:
        print(f"File not found: {code_path}")


@tool
def persist_transformed_file(dataset_id: str, filename: str, data_content: str):
    """
    Persists the transformed data to the local path.
    Pass params dataset_id, filename, data_content.
    """
    storage_path = os.getenv('STORAGE_PATH')
    code_path = os.path.join(storage_path, "datasets", dataset_id, "transformed", filename)
    try:
        with open(code_path, 'w') as file:
            file.write(data_content)
    except FileNotFoundError:
        print(f"File not found: {code_path}")


# @tool
def logger(dataset_id: str, log_string: str, filename="log"):
    """
    Logs the passed string to the dataset_id log file.
    :param dataset_id:
    :param log_string:
    :return:
    """
    storage_path = os.getenv('STORAGE_PATH')
    log_path = os.path.join(storage_path, "datasets", dataset_id, f'{filename}.txt')
    try:
        with open(log_path, 'a') as file:
            file.write(_DIVIDER)
            file.write(log_string)
    except FileNotFoundError:
        print(f"File not found: {log_path}")

@tool
def get_dataframe_agent(dataset_id, table, query):
    """Get analysis result using pandas dataframe agent.
    Pass dataset_id, table name and query to get dataframe analysis.
    Returns analysis result in string."""
    ds = get_dataset_info(dataset_id)
    df = None
    if 'csv' in ds['type']:
        if ds['sources']['files'][table]:
            df = pd.read_csv(ds['sources']['files'][table])

    if df:
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-4o"),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        agent.invoke(query)
    return None


python_repl = PythonREPL()
# You can create the tool to pass to an agent
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

anal_repl_tool = Tool(
    name="anal_python_repl",
    description="""A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.
    Your purpose is just for debugging/analysis purposes and not making actual change to the data source file.""",
    func=python_repl.run,
)

python_repl_tool = PythonREPLTool()

@tool
def run_command(command: str):
    """

    :param command:
    :return:
    """
    import subprocess
    try:
        env = os.environ.copy()
        result = subprocess.run(command.split(), capture_output=True, text=True, env=env)
        if result.stdout:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        print(e)
        return str(e)