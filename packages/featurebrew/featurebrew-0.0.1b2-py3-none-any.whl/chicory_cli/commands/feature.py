import json
import os
import sys

import click

from logging import basicConfig, getLogger, INFO

from chicory_tools.api_config import initialize_services
from chicory_cli.tools.utilities import get_base_classifier
from chicory_tools.metadata import _set_env, create_dataset_metadata
from services.data_explorer.tools import get_dataset_features
from services.feature_brew.components.dataset import FeatureBrewDataset
from services.feature_brew.components.sklearn_wrapper import FeatureBrewEstimator

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Generate and Extract Feature from Chicory FeatureBrew Dataset. ")
@click.option('--name', '-n', prompt='Enter the name of the dataset', help='alphanumeric string')
@click.option('--config', '-c', prompt='Chicory Configuration to define dataset and resources', help='refer the documentation')
@click.option('--query', '-q', prompt='User Question. Support: Classification', help='query for prediction')
@click.option('--context', '-a', prompt='Additional Context', help='additional-context')
def feature(name, config, query, context):
    # checks if dependency exists
    services = initialize_services(config)
    # Initialize services
    _set_env(services)

    persist_path = os.getenv('STORAGE_PATH')

    feature_recommendations = get_dataset_features(name)
    NUM_QUERY = 5 # Number of ensembles

    click.secho(f"Extracting Rules ...", fg='green')

    dataset = FeatureBrewDataset(dataset=name, data_source=f"{persist_path}/datasets",
                                 shot=feature_recommendations["training_shot"], seed=feature_recommendations["seed"])
    # df, X_train, X_test, y_train, y_test, target_attr, label_list, is_cat, X_all
    dataset.X_train.head(feature_recommendations["training_shot"])

    llm_base_classifier = get_base_classifier(feature_recommendations["task_class"])

    feature_brew_estimator = FeatureBrewEstimator(chicory_api_key=os.getenv("OPENAI_API_KEY"),
                                                  train_call_back=llm_base_classifier,
                                                  evaluate_dataset=False,
                                                  validate_features=True,
                                                  persist_rules=True,
                                                  evaluation_metric="auc")

    USER_PROMPT = f"""
        {query}

        {context}"""

    feature_brew_estimator.fit(dataset, target_attr=dataset.target_attr,
                               iterations=NUM_QUERY,
                               dataset_description=None,
                               task_desc=USER_PROMPT)

    click.secho(f"Generating Feature Functions ...", fg='green')

    fct_names, fct_strs_final = feature_brew_estimator.generate_feature_functions(dataset)
    executable_list, X_train_all_dict, X_test_all_dict = feature_brew_estimator.convert_to_binary_vectors(
        fct_strs_final, fct_names, dataset)

    result_auc = feature_brew_estimator.predict(dataset, executable_list, X_train_all_dict, X_test_all_dict)
    logger.info(f"Ensembled AUC: {str(result_auc)}")
    click.echo(f"Please find the result at: {persist_path}/datasets/{name}/features")
    click.secho("Feature Functions Generated.", fg='blue')
