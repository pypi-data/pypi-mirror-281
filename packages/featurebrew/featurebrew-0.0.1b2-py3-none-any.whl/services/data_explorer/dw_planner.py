import asyncio
import operator
import os
from typing import Annotated, List, Tuple, TypedDict, Literal, Union

from langchain_core.tools import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent
from pydantic import ValidationError

from services.data_explorer.tools import get_dataset_info, get_dataset_schema, logger, repl_tool, get_dataset_features, \
    get_dataset_processed_file_path

MODEL = os.getenv("MODEL", 'gpt-4o')



class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    dataset_id: str
    desc_schema: str
    response: str
    updated_code: str
    completed: bool


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
    completed: str = Field(
        description="flag to confirm task completion"
    )


class Response(BaseModel):
    """Response to user."""

    response: str
    completed: bool


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
                    "If you need to further use tools to get the answer, use Plan."
    )


def initialize_brewmind_wrangling_workflow():
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
                  "type": "<sqlite, csv, xlsx>", # right now, we only support 1 type for each dataset
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
        description="""Useful to get schema of dataset for answering user question. Always, pass correct dataset_id 
        value.""",
    ), Tool(
        name="DataSetFeatures",
        func=get_dataset_features,
        description="""Useful to get recommended relevant columns/features of dataset for answering user question, among
        all the relevant table(s). Use it as a hint. Always, pass correct dataset_id value.""",
    ), Tool(
        name="ProcessedDataSetFilePath",
        func=get_dataset_processed_file_path,
        description="""Useful to get processed dataset file path for answering user question. Always, pass correct 
        dataset_id value.""",
    ), repl_tool]

    # Choose the LLM that will drive the agent
    llm = ChatOpenAI(model=MODEL)
    agent_executor = create_react_agent(llm, tools, messages_modifier=prompt)

    planner_prompt_template = """As a data scientist/engineer, for the given objective of preparing dataset for 
    feature engineering, come up with a simple step by step plan. This plan should involve individual tasks, 
    that if executed correctly will yield the correct answer. Do not add any superfluous steps. The result of the final 
    step should be the final answer and should have used the final version of the updated_code for the transformed data. 
    Make sure that each step has all the information needed - do not skip steps. Consider leveraging the passed schema 
    for generating the plan. The goal is to come up with the final data transformation required for one consolidated 
    dataset.

    【Dataset Schema】
    {desc_schema}

    【Dataset Info】
    {dataset_info}

    Hints:
    * If there are multiple tables involved, choose one or more tables to be analyzed as per the user query requirements. 
    Ignore irrelevant tables, if applicable.
    * Statistically analyze relevant tables/files to find out the action needed for ml prediction.
    * Never have any prediction, model evaluation or training split of the data executed. Not needed.

    Notes:
    * make sure to have target attribute at the end of the table in the final data
    * if preparation not possible or needed, then respond accordingly
    * always remember, data wrangling includes discovery, structuring, cleaning, enriching and transforming data
    * never apply any transformation to the source file or any file which you have not created
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
        model=MODEL, temperature=0
    ).with_structured_output(Plan)

    replanner_prompt_template = """For the given objective, as an expert data scientist/engineer, of preparing dataset, 
    come up with a simple step by step plan. This plan should involve individual tasks, that if executed correctly will 
    yield the correct answer. Do not add any superfluous steps. The result of the final step should have used the final 
    version of the updated_code for the transformed data. Make sure that each step has all the information needed - do 
    not skip steps. According to the analysis of the data, modify the plans by adding or removing other detailed analysis 
    steps. Your goal is to validate the planner by analysing the data, as per each step and finalize the transformation 
    code for feature extraction accordingly. The ultimate goal is to have a final data transformation into one 
    consolidated dataset. Final response should include the final transformation code as the updated_code.

    Additional final steps:
    * Make sure that the final transformation is only processing relevant tables and columns as per the user query 
    requirements.

    Hint:
    * Do not perform any prediction, model evaluation, or training split of the data.
    * Each step should focus on analyzing and updating the transformation code without writing anything to disk.
    * Establish semantic connections between tables if necessary.
    * Continuously update updated_code after each transformation to the dataset.
    * Do not apply any transformations to the source file or any file that you did not create.
    * Ensure that all steps are performed correctly and nothing is left unfinished before considering the process complete.
    * If a step with the same execution result has already been performed, skip it.
    * If any step fails, attempt fixes before completely failing.
    * Do not repeat any previously executed steps if a step fails. Avoid rerunning the same plan multiple times.
    * Always use the full path from past responses when loading any file or table within a dataset.
    * Generate a normalized version of the data if applicable to the problem statement.

    Your objective was this:
    {input}

    Your original plan was this:
    {plan}

    You have currently done the follow steps:
    {past_steps}

    【Current Dataset】
    {dataset_id}

    【Dataset Schema】
    {desc_schema}

    【Transformation Code】
    {updated_code}
    ==========

    Update your plan accordingly. If all the steps are executed/confirmed or no more steps are needed and you can return 
    to the user, then respond (including final updated_code) with that. Otherwise, fill out the plan. Only add steps to 
    the plan that still NEED to be completed. Do not return previously completed steps in the plan."""

    replanner_prompt = ChatPromptTemplate.from_template(replanner_prompt_template)

    # Update your plan accordingly. If no more steps are needed, you have validated `updated_code` -> you can pass the CodeExecResponse with final code to run (generate processed data) and response you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.
    replanner = replanner_prompt | ChatOpenAI(
        model=MODEL, temperature=0
    ).with_structured_output(Act)

    validator_prompt_template = """
    As an expert data engineer and python code specialist, your objective here is to make sure that the last transformation
    code was successfully executed and validate that the expected dataset is generated successfully.

    Hints:
    * If the code failed last time, use the response to deduce the fix and execute the code accordingly.
    * If you modify the code, also update `updated_code` with the latest version.

    【Last Code Execution】
    {response}

    ==========
    Update your response accordingly. If no more steps are needed and you can return to the user, then respond with that and 
    mark completed as True. Otherwise, fill out the plan and mark completed as False.
    """

    validator_prompt = ChatPromptTemplate.from_template(validator_prompt_template)

    # Update your plan accordingly. If no more steps are needed, you have validated `updated_code` ->
    # you can pass the CodeExecResponse with final code to run (generate processed data) and response you can
    # return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan
    # that still NEED to be done. Do not return previously done steps as part of the plan.
    validator = validator_prompt | ChatOpenAI(
        model=MODEL, temperature=0
    ).with_structured_output(Act)

    async def execute_step(state: PlanExecute):
        plan = state["plan"]
        dataset_id = state["dataset_id"]
        plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""dataset_id={dataset_id}, for the following plan:
    {plan_str}\n\nYou are tasked with validating step {1} and returning the 
    transformation code to apply the same, if applicable, {task}."""
        logger(dataset_id, plan_str + "\n\n" + state["updated_code"]
               + "\n\n Current Task: \n" + task_formatted, "log_planner_steps")
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": (task, agent_response["messages"][-1].content),
        }

    async def execute_coder(state: PlanExecute):
        # past_steps = state["past_steps"]
        # final_code = state["updated_code"]
        final_code = state["response"]
        # plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(past_steps))
        task = (f"You are tasked with validating, updating and executing the transformation python code "
                f"successfully. \n\n {final_code}")
        task_formatted = f"""{task}
    \n\n Validate if the transformed data file exists before completing. Set `completed` to True when the code execution 
    is successful."""
        # \n\n==========
        # \n\nReference: {plan_str}"""
        #     logger(dataset_id, plan_str + "\n\n" + "\n\n Executing Code: \n" + task_formatted)
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "response": f"""{task_formatted}\n\n=========\n[Response]\n\n
            {agent_response["messages"][-1].content}""",
        }

    async def plan_step(state: PlanExecute):
        plan = await planner.ainvoke({"messages": [("user", state["input"])]})
        return {"plan": plan.steps, "dataset_id": plan.dataset_id, "desc_schema": plan.desc_schema,
                "updated_code": plan.updated_code}

    async def validate_code(state: PlanExecute):
        output = await validator.ainvoke(state)
        return {"response": output.action.response, "completed": output.action.completed}

    async def replan_step(state: PlanExecute):
        dataset_id = state["dataset_id"]
        output = await replanner.ainvoke(state)
        processed_path = os.path.join(os.getenv('STORAGE_PATH'), "datasets", dataset_id, dataset_id + "-processed.csv")
        if isinstance(output.action, Response):
            # pprint (output.action.updated_code)
            response = f"""For dataset_id={dataset_id}, MUST modify the code to update the final data location to
                                     {processed_path}, if applicable.\n\n{output.action.response}"""
            return {"response": response, "completed": False}
        else:
            try:
                return {"plan": output.action.steps, "dataset_id": output.action.dataset_id,
                        "desc_schema": output.action.desc_schema, "updated_code": output.action.updated_code}
            except ValidationError as e:
                if output.action.response:
                    response = f"""For dataset_id={dataset_id}, MUST modify the code to update the final data location to
                             {processed_path}, if applicable.\n\n{output.action.response}"""
                    return {"response": response, "completed": False}
                else:
                    raise e

    def should_validate(state: PlanExecute) -> Literal["agent", "__end__"]:
        if "response" in state and state["response"]:
            return "coder"
        else:
            return "agent"

    def should_end(state: PlanExecute) -> Literal["agent", "__end__"]:
        if "completed" in state and state["completed"]:
            return "__end__"
        else:
            return "coder"
    from langgraph.graph import StateGraph

    workflow = StateGraph(PlanExecute)

    # Add the plan node
    workflow.add_node("planner", plan_step)

    # Add the validation step
    workflow.add_node("agent", execute_step)

    # Add a replan node
    workflow.add_node("replan", replan_step)

    # Add a code validator node
    workflow.add_node("validator", validate_code)

    # Add the code execution step
    workflow.add_node("coder", execute_coder)

    workflow.set_entry_point("planner")

    # From plan we go to agent
    workflow.add_edge("planner", "agent")

    # From agent, we replan
    workflow.add_edge("agent", "replan")

    # From coder, we validate
    workflow.add_edge("coder", "validator")

    workflow.add_conditional_edges(
        "replan",
        # Next, we pass in the function that will determine which node is called next.
        should_validate,
        {"coder": "coder", "agent": "agent"}
    )

    # Add conditional edges for coder to loop back to itself or end
    workflow.add_conditional_edges(
        "validator",
        should_end,
        {"coder": "coder", "__end__": "__end__"}
    )

    # From coder, we end
    workflow.add_edge("coder", "__end__")

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    app = workflow.compile()

    # from IPython.display import Image, display
    #
    # display(Image(app.get_graph(xray=True).draw_mermaid_png()))

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
