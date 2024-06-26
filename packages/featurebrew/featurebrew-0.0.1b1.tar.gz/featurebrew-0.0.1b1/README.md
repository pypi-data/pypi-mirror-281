# Chicory AI Feature Brew CLI

Command line tool for configuring and accessing Chicory autopilot data engineer

```shell
## Usage
> Usage: featurebrew [OPTIONS] COMMAND [ARGS]...
>
>   [Experimental] CLI tool to access Chicory autopilot data engineer
>
> Options:
>   --help  Show this message and exit.
>
> Commands:
>   create   Create Chicory FeatureBrew Dataset.
>   feature  Generate and Extract Feature from Chicory FeatureBrew Dataset.
>   prepare  Prepare Chicory FeatureBrew Dataset for Feature Extraction.
```


## Configuration file format:
```yaml
openai:
  open_api_key: "###"
  model: "gpt-4o"

persistence:
  storage_type: 'local'
  storage_path: "<local-path-for-featurebrew-datasets>"
```

## Sample Usage:
```shell
# The feature engineering using featurebrew is defined by steps:
Data Discovery -> Extraction -> Integration -> Feature engineering

# For this example:
# We have used openml health dataset (heart, myocardial, diabetes)
# the prediction (decision-tree) use-case is classification

# Step 1: Creating featurebrew dataset
# Required params: dataset name, configuration, source directory consisting of data files
# Current Support: CSV files
❯ featurebrew create --name "ml-dataset-internal" --config ./chicory-config.yaml --source ./datasets
Copied: datasets/heart.csv to ./datasets/ml-dataset-internal/source/heart.csv
Copied: datasets/myocardial.csv to ./datasets/ml-dataset-internal/source/myocardial.csv
Copied: datasets/diabetes.csv to ./datasets/ml-dataset-internal/source/diabetes.csv
Dataset Created.

# Step 2: Preparing dataset for feature engineering
# Required params: dataset name, configuration, query (use-case) for prediction
# Optional param: hint (for finding relevant tables)
❯ featurebrew prepare --name "ml-dataset-internal" --config "chicory-config.yaml" --query """Does this patient have diabetes? Yes or no?"""
Analysing Dataset ...
load json file from ./datasets/ml-dataset-internal/tables.json
Preparing Dataset ...
WARNING:langchain_experimental.utilities.python:Python REPL can execute arbitrary code. Use with caution.
Please find the dataset at: ./datasets/ml-dataset-internal/ml-dataset-internal-processed.csv
Dataset Prepared.

# Step 2: Preparing dataset for feature engineering
# Required params: dataset name, configuration, query (use-case) for prediction, additional-context for feature extraction
❯ featurebrew feature --name "ml-dataset-internal" --config "chicory-config.yaml" --query """Does this patient have diabetes? Yes or no?""" --context """Several constraints were placed on the selection of these instances from\n    a larger database. In particular, all patients here are females at\n    least 21 years old of Pima Indian heritage. ADAP is an adaptive learning\n    routine that generates and executes digital analogs of perceptron-like\n    devices. It is a unique algorithm; see the paper for details.\n    \n    Use AUC for evaluating the generated features.\n"""
Extracting Rules ...
Fetching datatset info:

{'Pregnancies': 'number of pregnancies', 'Glucose': 'glucose level', 'BloodPressure': 'blood pressure', 'SkinThickness': 'skin thickness', 'Insulin': 'insulin level', 'BMI': 'body mass index', 'DiabetesPedigreeFunction': 'diabetes pedigree function', 'Age': 'age of the patient', 'Outcome': 'diabetes outcome (yes or no)'}
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:33<00:00,  6.62s/it]
Generating Feature Functions ...
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:11<00:00,  5.59s/it]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.22s/it]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:09<00:00,  4.70s/it]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:09<00:00,  4.77s/it]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:08<00:00,  4.18s/it]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:46<00:00,  9.38s/it]
INFO:chicory_cli.commands.feature:Ensembled AUC: 0.6962962962962963
Please find the result at: ./datasets/ml-dataset-internal/features
Feature Functions Generated.

```