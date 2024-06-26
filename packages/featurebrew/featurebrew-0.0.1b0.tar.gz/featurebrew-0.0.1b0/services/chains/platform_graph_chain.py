import dotenv
import os

from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


PLATFORM_QA_MODEL = os.getenv("PLATFORM_QA_MODEL")
PLATFORM_CYPHER_MODEL = os.getenv("PLATFORM_CYPHER_MODEL")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

graph.refresh_schema()

cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement. If you need to divide numbers, make sure to
filter the denominator to be non zero. Confirm for any value if missing.
Also note, Region.id is formed by adding `account`-`aws_region`
Also note, Spark Jobs are represented as EMRSteps in AWS world

Examples:
# How many accounts do I have with aws?
MATCH (p:Provider)-[:HAS]->(a:Account)
WHERE p.id="aws"
RETURN COUNT(a) AS NumberOfAccounts
LIMIT 1

# How many emr clusters do I have in my carbonara aws account in us-west-1?
# region_id is formed using account_id and aws region names
MATCH (p:Provider)-[:HAS]->(a:Account)-[:HAS]->(r:Region)-[:HAS]->(e:EMRCluster)
WHERE p.id="aws" AND a.id="carbonara" AND r.id="carbonara-us-west-1"
RETURN COUNT(e) AS EMRClusterCount
LIMIT 1

# What is the current status of the Spark job with ID s-05764882GAK11NOAOC92 on EMR cluster j-2CGRRXO3FXIED?
MATCH (e:EMRCluster)-[:HAS]->(s: EMRStep)
WHERE e.id = 'j-2CGRRXO3FXIED' AND s.id = 's-05764882GAK11NOAOC92'
RETURN s.statusState
LIMIT 1

# Can you provide the execution timeline of the Spark job s-05764882GAK11NOAOC92 on EMR cluster j-2CGRRXO3FXIED?
MATCH (e:EMRCluster)-[:HAS]->(s: EMRStep)
WHERE e.id = 'j-2CGRRXO3FXIED' AND s.id = 's-05764882GAK11NOAOC92'
RETURN s.statusCreationDateTime, s.statusReadyDateTime, s.statusEndDateTime
LIMIT 1

# What are the last tests which failed in my aws account clusters?
MATCH (p:Provider)-[:HAS]->(a:Account)-[:HAS]->(r:Region)-[:HAS]->(e:EMRCluster)-[:HAS]->(s:EMRStep)
WHERE p.id="aws" AND s.statusState="FAILED"
RETURN e.id AS EMRClusterID, s.id AS EMRStepID, s.name AS EMRStepName, s.statusEndDateTime AS FailedDateTime
ORDER BY s.statusEndDateTime DESC


# Tell me the schema of the data sources of Spark job s-05764882GAK11NOAOC92
MATCH (s: EMRStep)
WHERE s.id = 's-05764882GAK11NOAOC92'
RETURN s.configJar, s.configProperties, s.configArgs
LIMIT 1
# Use the s3 paths in response to retrieve data from platform_data_chain

If there is a question about s3 path or source data, please pass the response to platform_data_chain to handle

Hint:
# Make sure to use IS NULL or IS NOT NULL when analyzing missing properties.
# Never return embedding properties in your queries. You must never include the
statement "GROUP BY" in your query. Make sure to alias all statements that
follow as with statement.
# If you need to divide numbers, make sure to filter the denominator to be non
zero.

The question is:
{question}
"""

cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a users natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must provide an answer using the
results. If the question involves a time duration, assume the query
results are in units of minutes unless otherwise specified.

If the query failed, you either try to rerun the query or provide a
message to user to re-run the query.

When there is any PII or identifiable variable, mask it and 
mention it in the footer. When long strings are provided 
in the query results, beware of the structure that have commas or other
punctuation in them. For instance, '["spark-submit", "--deploy-mode", "cluster", 
"s3://ss-datapipeline-batch-source/health_violations.py", "--data_source",
"s3://ss-datapipeline-batch-source/data/food_establishment_data.csv", 
"--output_uri", "s3://ss-datapipeline-batch-source/output"]' is technically 
a string representing an array is a complete configuration with multiple 
argument parameters not single.

Hint:
# Make sure you return any list of values in a way that isn't ambiguous.
# Never say you don't have the right information if there is data in
the query results.
# Make sure to show all the relevant query results if you're asked.

Helpful Answer:
"""

qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)

platform_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=PLATFORM_CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=PLATFORM_QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
)
