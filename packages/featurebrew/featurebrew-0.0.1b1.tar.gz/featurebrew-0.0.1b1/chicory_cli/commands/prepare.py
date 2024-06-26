import asyncio
import json
import os
import sys

import click

from logging import basicConfig, getLogger, INFO

from pydantic import ValidationError

from chicory_tools.api_config import initialize_services
from chicory_tools.metadata import _set_env, create_dataset_metadata
from services.data_explorer.dw_planner import initialize_brewmind_wrangling_workflow
from services.sql_generator.agents.selector import initialize_selector_agent
from services.sql_generator.const import SELECTOR_NAME, di_selector_template

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Prepare Chicory FeatureBrew Dataset for Feature Extraction.")
@click.option('--name', '-n', prompt='Enter the name of the dataset', help='alphanumeric string')
@click.option('--config', '-c', prompt='Chicory Configuration to define dataset and resources', help='refer the documentation')
@click.option('--query', '-q', prompt='User Question. Support: Classification', help='query for prediction')
@click.option('--hint', '-h', default='', help='data hint for table selection')
def prepare(name, config, query, hint):
    # checks if dependency exists
    services = initialize_services(config)
    # Initialize services
    _set_env(services)

    persist_path = os.getenv('STORAGE_PATH')

    # Step 2: Derive relevant table schema using SELECTOR
    message = {
        "db_id": name,
        "extracted_schema": {},
        "evidence": hint,
        "query": query,
        "send_to": SELECTOR_NAME
    }

    click.secho(f"Analysing Dataset ...", fg='green')

    selector_data_agent = initialize_selector_agent(data_path=f"{persist_path}/datasets/{name}/source",
                                                    tables_json_path=f"{persist_path}/datasets/{name}/tables.json",
                                                    prompt_template=di_selector_template,
                                                    lazy=True)

    selector_data_chain_message = selector_data_agent.invoke(message)
    # 2 in total
    for i in range(1):
        selector_data_chain_message = selector_data_agent.invoke(selector_data_chain_message)
    # print(selector_data_chain_message)

    with open(f"{persist_path}/datasets/{name}/schema.json", 'w') as json_file:
        dict = str(selector_data_chain_message["chosen_db_schem_dict"]).replace("{", "{{").replace("}", "}}")
        json.dump(dict, json_file, indent=4)
        # json_file.write(dict)
        json_file.write("\n\n## Table Schema Description\n\n")
        json_file.write(selector_data_chain_message["desc_str"])

    with open(f"{persist_path}/datasets/{name}/{name}-metadata.json", 'w') as json_file:
        json.dump(selector_data_chain_message["metadata"], json_file, indent=4)

    with open(f"{persist_path}/datasets/{name}/{name}-features.json", 'w') as json_file:
        json.dump(selector_data_chain_message["features"], json_file, indent=4)

    feature_recommendations = selector_data_chain_message["features"]

    if feature_recommendations["problem_type"] != "classification":
        click.secho(f"Problem Type not supported!! {feature_recommendations["problem_type"]}", fg='red')
        sys.exit(1)

    click.secho(f"Preparing Dataset ...", fg='green')

    async def main():
        try:
            app = initialize_brewmind_wrangling_workflow()
            config = {"recursion_limit": 100}
            inputs = {
                "input": f"For dataset_id={name}, prepare data for `{query}`."}

            async for event in app.astream(inputs, config=config):
                try:
                    for k, v in event.items():
                        if k != "__end__":
                            logger.debug(v)
                except Exception as e:
                    logger.error(f"Error processing event: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Error in main workflow: {e}", exc_info=True)

    asyncio.run(main())

    # lets check if the dataset was generated
    storage_path = os.getenv('STORAGE_PATH')
    processed_path = os.path.join(storage_path, "datasets", name, name + "-processed.csv")
    if not os.path.exists(processed_path):
        click.echo("Failed to prepare dataset. Try again.")
    else:
        click.echo(f"Please find the dataset at: {processed_path}")
        click.secho(f"Dataset Prepared.", fg='blue')

