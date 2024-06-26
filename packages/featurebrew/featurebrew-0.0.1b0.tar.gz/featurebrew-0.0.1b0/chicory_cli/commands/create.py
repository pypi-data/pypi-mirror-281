import os

import click

from logging import basicConfig, getLogger, INFO

from chicory_tools.api_config import initialize_services
from chicory_tools.metadata import _set_env, create_dataset_metadata

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)

@click.command(help="Create Chicory FeatureBrew Dataset.")
@click.option('--name', '-n', prompt='Enter the name of the dataset to define', help='alphanumeric string')
@click.option('--config', '-c', prompt='Chicory Configuration to define dataset and resources', help='refer the documentation')
@click.option('--source', '-s', prompt='Dataset datasource folder. Support: CSV', help='refer the documentation')
def create(name, config, source):
    # checks if dependency exists
    services = initialize_services(config)
    # Initialize services
    _set_env(services)

    create_dataset_metadata(name, source, services)
    click.secho("Dataset Created.", fg='blue')