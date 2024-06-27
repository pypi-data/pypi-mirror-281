import asyncio
import operator
from typing import Annotated, List, Tuple, TypedDict, Literal, Union

from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from services.data_explorer.tools import get_dataset_info, get_dataset_schema, anal_repl_tool, logger


# Get the prompt to use - you can modify this!
prompt = hub.pull("wfh/react-agent-executor")
# prompt.pretty_print()

tools = [Tool(
    name="DataSetInfo",
    func=get_dataset_info,
    description="""Useful to get location of each related dataset files/tables for answering user question.
            Always, pass correct dataset_id value.
            Output format:
            {
              "ds_id": "<>",
              "type": "<sqllite, csv, xlsx>", # right now, we only support 1 type for each dataset
              "sources": {
                "type": "s3",
                "paths": [
                  {"file_name1": "<file_path_1>"},
                  {"file_name2": " <file_path_2>"},
                ]
              }
            }
            """,
), Tool(
    name="DataSetSchema",
    func=get_dataset_schema,
    description="""Useful to get schema of dataset for answering user question. Always, pass correct dataset_id value.""",
), anal_repl_tool]

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-4o")
agent_executor = create_react_agent(llm, tools, messages_modifier=prompt)

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    dataset_id: str
    desc_schema: str
    response: str
    updated_code: str
    input_file_path: List[str]
    output_file_path: List[str]


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )
    dataset_id: str = Field(
        description="dataset id in string format"
    )
    desc_schema: str = Field(
        description="dataset schema description in string format"
    )
    updated_code: str = Field(
        description="python code file content in string"
    )
    input_file_path: List[str] = Field(
        description="all relevant input dataset sources"
    )
    output_file_path: List[str] = Field(
        description="generated dataset from the input and transformation in the last step"
    )

planner_prompt_template = """As a data scientist/engineer, for the given objective of cleaning/preparing dataset for 
prediction, come up with a simple step by step plan. This plan should involve individual tasks, that if executed 
correctly will yield the correct answer. Do not add any superfluous steps. 
The result of the final step should be the final answer and should have used the final version of the updated_code for 
the transformed data. Make sure that each step has all the information needed - do not skip steps.
Consider leveraging the passed schema for generating the plan. The goal is to come up with the final data transformation
required. Set `output_file_path`, as the initial list of relevant table files (from dataset_info), this plan should be 
executed on.

【Relevant Dataset Schema】
{desc_schema}

{dataset_info}

Hints:
* `output_file_path` should be an existing full file path on disk
* If there are multiple tables involved, choose one or more tables to be analyzed as per the user query requirements. 
Ignore irrelevant tables, if applicable
* Statistically analyze relevant tables/files to find out the action needed for ml prediction
* Never apply any transformation to the source file or any file which you have not created
* Never have any prediction, model evaluation or training split of the data executed. Not needed

Notes:
* make sure to have target attribute at the end of the table in the final data
* if preparation not possible or needed, then respond accordingly
* always remember, data wrangling includes discovery, structuring, cleaning, enriching, validating and transforming data

This is a typical example:
==========
input: For dataset_id=ml-dataset-internal, prepare data for `Does this patient have diabetes? Yes or no?`

output:
plan:
  - Step 1: Load the 'diabetes' table from the dataset 'ml-dataset-internal'.
  - Step 2: Inspect the dataset for any missing values and handle them appropriately (e.g., imputation, removal).
  - Step 3: Convert categorical columns (if any) to numerical values using encoding techniques (e.g., label encoding, 
  one-hot encoding).
  - Step 4: Normalize or standardize numerical features to ensure they are on a similar scale.
  - Step 5: Ensure the target attribute 'Outcome' is at the end of the table.
  - Step 6: Validate the cleaned and prepared dataset to ensure there are no inconsistencies or errors.
dataset_id: ml-dataset-internal
desc_schema: ```"hello": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", 
"DiabetesPedigreeFunction", "Age", "Outcome"]```
output_file_path:
  - '/tmp/chicory/datasets/ml-dataset-internal/source/diabetes.csv'
  - '/tmp/chicory/datasets/ml-dataset-internal/source/myocardial.csv'
  - '/tmp/chicory/datasets/ml-dataset-internal/source/heart.csv'
"""


planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", planner_prompt_template.format(desc_schema=get_dataset_schema("ml-dataset-internal"),
                                                     dataset_info=str(get_dataset_info("ml-dataset-internal"))
                                                     .replace("{", "{{").replace("}", "}}")),
        ),
        ("placeholder", "{messages}"),
    ]
)
planner = planner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Plan)


class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
                    "If you need to further use tools to get the answer, use Plan."
    )


replanner_prompt_template = """For the given objective, as an expert data scientist/engineer, of cleaning/preparing 
dataset(s) for prediction, come up with a simple step by step plan. for the given objective of writing a data 
transformation code in python, for cleaning/preparing dataset for prediction, come up with a simple step by step plan. 
This plan should involve individual tasks, that if executed correctly will yield the correct answer. 
Do not add any superfluous steps. 
The result of the final step should be the final answer and should have used the final version of the updated_code for 
the transformed data. Make sure that each step has all the information needed - do not skip steps.
According to the analysis of the data, modify the plans by adding or removing detailed analysis steps. Your goal is to 
execute the planner and prepare (transform) the data for feature extraction. The ultimate goal is to have a final 
dataset file.
For execution, each step should refer `input_file_path` and set `output_file_path`, after any transformation, if 
applicable or set output_file_path=input_file_path, if not transformation took place

Additional final steps:
* Make sure to validate and execute the `updated_code` transformation, validate the data and ultimately
persist the transformation data to os.path.join(os.getenv('STORAGE_PATH'),'datasets',<dataset_id>,<dataset_id>-processed}}.csv)
and set output_file_path accordingly.
* When responding that the data has been persisted, make sure to share the full path after validating if the file 
actually exists.
* Never have any prediction, model evaluation or training split of the data executed. Not needed. 

Hint:
* `input_file_path` and `output_file_path` should be an existing full file path on disk
* All the steps should analyse and update the transformation code and never write anything to disk 
* suffix every step with `Update the transformation code with the actions of this step.`
* You can make semantic connections between tables if needed
* Make sure to load all the tables as per the provided schema and create a consolidated dataset
* Update updated_code after each transformation to the dataset, for the next step to pick up as source
* Never apply any transformation to the source file or any file which you have not created
* Before responding with process completion, make sure all steps are performed correctly and nothing is left
* If the current step with same execution result is in the past step list, skip it.
* Don't start from step 1 again if last step failed -> don't repeat all the previous steps again. 
Avoid rerunning same plan multiple times
* if any step fails, try some fixes before failing completely  
* For loading any file/table inside a dataset, always use the full path from past responses
* Always generate normalized version of the data, if applicable to the problem statement

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

【Current Dataset】
{dataset_id}

【Relevant Dataset Schema】
{desc_schema}

【Last Transformation Code】
{updated_code}
==========

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond (including
output_file_path) with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. 
Do not return previously done steps as part of the plan.

This is a typical example:
==========
input: For dataset_id=ml-dataset-internal, prepare data for `Does this patient have diabetes? Yes or no?`

plan:
  - Step 1: Load the 'diabetes' table from the dataset 'ml-dataset-internal'.
  - Step 2: Inspect the dataset for any missing values and handle them appropriately (e.g., imputation, removal).
  - Step 3: Convert categorical columns (if any) to numerical values using encoding techniques (e.g., label encoding, 
  one-hot encoding).
  - Step 4: Normalize or standardize numerical features to ensure they are on a similar scale.
  - Step 5: Ensure the target attribute 'Outcome' is at the end of the table.
  - Step 6: Validate the cleaned and prepared dataset to ensure there are no inconsistencies or errors.
dataset_id: ml-dataset-internal
desc_schema: ```{{"hello": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", 
"DiabetesPedigreeFunction", "Age", "Outcome"]}}```
input_file_path:
  - /tmp/chicory/datasets/ml-dataset-internal/source/diabetes.csv
  - /tmp/chicory/datasets/ml-dataset-internal/source/myocardial.csv
  - /tmp/chicory/datasets/ml-dataset-internal/source/heart.csv
output_file_path:
  - /tmp/chicory/datasets/ml-dataset-internal/processed/ml-dataset-internal_cleaned.csv
"""

replanner_prompt = ChatPromptTemplate.from_template(replanner_prompt_template)

# Update your plan accordingly. If no more steps are needed, you have validated `updated_code` -> you can pass the CodeExecResponse with final code to run (generate processed data) and response you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.
replanner = replanner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Act)


async def execute_step(state: PlanExecute):
    plan = state["plan"]
    dataset_id = state["dataset_id"]
    plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
    task = plan[0]
    task_formatted = f"""dataset_id={dataset_id}, for the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    logger(dataset_id, plan_str + "\n\n" + state["updated_code"])
    agent_response = await agent_executor.ainvoke(
        {"messages": [("user", task_formatted)]}
    )
    return {
        "past_steps": (task, agent_response["messages"][-1].content),
    }


async def plan_step(state: PlanExecute):
    plan = await planner.ainvoke({"messages": [("user", state["input"])]})
    return {"plan": plan.steps, "dataset_id": plan.dataset_id, "desc_schema": plan.desc_schema,
            "updated_code": plan.updated_code, "input_file_path": plan.input_file_path,
            "output_file_path": plan.input_file_path}


async def replan_step(state: PlanExecute):
    output = await replanner.ainvoke(state)
    if isinstance(output.action, Response):
        return {"response": output.action.response}
    else:
        return {"plan": output.action.steps, "dataset_id": output.action.dataset_id,
                "desc_schema": output.action.desc_schema, "updated_code": output.action.updated_code,
                "input_file_path": output.action.output_file_path, "output_file_path": output.action.output_file_path}


def should_end(state: PlanExecute) -> Literal["agent", "__end__"]:
    if "response" in state and state["response"]:
        return "__end__"
    else:
        return "agent"


def initialize_brewmind_wrangling_workflow():
    from langgraph.graph import StateGraph

    workflow = StateGraph(PlanExecute)

    # Add the plan node
    workflow.add_node("planner", plan_step)

    # Add the execution step
    workflow.add_node("agent", execute_step)

    # Add a replan node
    workflow.add_node("replan", replan_step)

    workflow.set_entry_point("planner")

    # From plan we go to agent
    workflow.add_edge("planner", "agent")

    # From agent, we replan
    workflow.add_edge("agent", "replan")

    workflow.add_conditional_edges(
        "replan",
        # Next, we pass in the function that will determine which node is called next.
        should_end,
    )

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    app = workflow.compile()
    return app


async def main():
    app = initialize_brewmind_wrangling_workflow()
    config = {"recursion_limit": 100}
    inputs = {
        "input": "For dataset_id=ml-dataset-internal, prepare data for `Does this patient have diabetes? Yes or no?`"}

    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)


if __name__ == "__main__":
    asyncio.run(main())