import dotenv
import os
import sys

from logging import basicConfig, getLogger, DEBUG

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=DEBUG, format=formatter)
logger = getLogger(__name__)

dotenv.load_dotenv("../resources/.env")


from fastapi import FastAPI
from utils.async_utils import async_retry
from models.sql_gen_query import SQLGenQueryInput, SQLGenQueryOutput
from sql_generator.agents.chat_manager import ChatManager
from sql_generator.const import SYSTEM_NAME

def _fail_if_undefined(var: str):
    if not os.environ.get(var):
        logger.error(f"ENV Var: '{var}' is not defined")
        sys.exit((1))


# _fail_if_undefined("OPENAI_API_KEY")
# _fail_if_undefined("DATA_DB_PATH")
# _fail_if_undefined("DATA_DB_COLLECTION")
# _fail_if_undefined("AWS_ACCESS_KEY_ID")
# _fail_if_undefined("AWS_SECRET_ACCESS_KEY")
# _fail_if_undefined("NEO4J_URI")
# _fail_if_undefined("NEO4J_USERNAME")
# _fail_if_undefined("NEO4J_PASSWORD")
# _fail_if_undefined("PLATFORM_QA_MODEL")
# _fail_if_undefined("PLATFORM_CYPHER_MODEL")
# _fail_if_undefined("PLATFORM_CODE_MODEL")
# _fail_if_undefined("PLATFORM_AGENT_MODEL")

# add tracing in LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Multi-agent Collaboration text2SQL"


app = FastAPI(
    title="BrewMind Chatbot",
    description="Chicory AI Agent powered Data Platform",
)


@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(db_id: str, query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """

    db_path = os.getenv('DS_PATH')
    test_manager = ChatManager(data_path=f"{db_path}/database",
                               log_path="",
                               tables_json_path=f"{db_path}/tables.json",
                               lazy=True)

    msg = {
        "db_id": db_id,
        "extracted_schema": {},
        "evidence": "",
        "query": query,
        "send_to": SYSTEM_NAME
    }
    test_manager.start(msg)
    return {"input": query, "explanation": msg["desc_str"], "output": msg['pred']}


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/chicory-sql-agent")
async def ask_platform_agent(query: SQLGenQueryInput) -> SQLGenQueryOutput:
    query_response = await invoke_agent_with_retry(query.db_id, query.text)
    # query_response["intermediate_steps"] = [
    #     str(s) for s in query_response["intermediate_steps"]
    # ]

    return query_response
