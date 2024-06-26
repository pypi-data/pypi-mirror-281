import yaml


class ConfigLoader:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

def initialize_services(config_path='config.yaml'):
    config_loader = ConfigLoader(config_path)
    config = config_loader.config

    # Initialize AWS Services with the AWS part of the config
    s3_config = config.get('s3', {})
    redshift_config = config.get('redshift', {})

    # Initialize GitHub service
    github_config = config.get('github', {})
    api_token = github_config.get('api_token')

    # Initialize GCP BigQuery
    bigquery_config = config.get('bigquery', {})

    # Initialize Snowflake service
    snowflake_config = config.get('snowflake', {})
    # snowflake_service = SnowflakeAccess(**snowflake_config)

    # Initialize local data set
    local_dataset_config = config.get('local_dataset', {})

    # Initialize Knowledge Graph
    neo4j_config = config.get('neo4j', {})
    embed_db_config = config.get('embed_db', {})

    # Initialize OpenAI service
    openai_config = config.get('openai', {})
    api_key = openai_config.get('api_key')
    # openai_service = OpenAI(api_key)

    # Initialize data persistence client
    persistence_config = config.get('persistence', {})

    # Return initialized services or add them to a class attribute if using within a class
    return {
        'integration': {
            's3': s3_config,  # Replace with your initialized service if applicable
            'redshift': redshift_config,
            'github_token': api_token,  # Replace with your initialized service if applicable
            'bigquery': bigquery_config,
            'local_dataset': local_dataset_config,
            'snowflake': snowflake_config,  # Replace with your initialized service if applicable
        },
        'system': {
            'openai': openai_config,  # Replace with your initialized service if applicable
            'neo4j': neo4j_config,  # Replace with your initialized service if applicable
            'persistence': persistence_config,
        }
    }