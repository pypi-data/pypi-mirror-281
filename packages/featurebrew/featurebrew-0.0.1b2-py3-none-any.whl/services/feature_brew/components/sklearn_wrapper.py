import ast
import os
from logging import getLogger

import openai
import torch
import torch.nn.functional as F
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.base import BaseEstimator
from sklearn.metrics import roc_auc_score, accuracy_score

from services.feature_brew.featureset_agent import FeatureSetAgent
from services.feature_brew.components.training import base_classifier
from services.feature_brew.components.validate import check_ast

_DIVIDER = "\n\n---=======---\n\n"
_VERSION = "\n\n---+++++++---\n\n"
_MODEL = os.getenv("MODEL", 'gpt-4o')
logger = getLogger(__name__)

class FeatureBrewEstimator(BaseEstimator):
    def __init__(
            self,
            chicory_api_key,
            train_call_back=base_classifier,
            evaluate_dataset=False,
            validate_features=True,
            persist_rules=True,
            evaluation_metric="auc",
    ) -> None:
        self.chicory_api_key = chicory_api_key
        openai.api_key = chicory_api_key
        self.train_call_back = train_call_back
        self.evaluate_dataset = evaluate_dataset
        self.validate_features = validate_features
        self.persist_rules = persist_rules
        self.evaluation_metric = evaluation_metric

        self.chicory_featureset_agent = FeatureSetAgent()

    def fit(self, dataset, target_attr, iterations, task_desc, dataset_description=None):
        meta_data_name = f"{dataset.data_source}/{dataset.dataset_name}/{dataset.dataset_name}-metadata.json"
        self.templates, self.feature_desc = self.chicory_featureset_agent.get_prompt_for_asking(
            dataset, target_attr, meta_data_name, task_desc, num_query=iterations
        )
        self._generate_rules(dataset)

    def _generate_rules(self, dataset):
        rule_file_name = f'{dataset.data_source}/{dataset.dataset_name}/features/rule-{dataset.dataset_name}-{dataset.shot}-{dataset.seed}.out'
        if os.path.isfile(rule_file_name) == False:
            self.results = self.chicory_featureset_agent.query_gpt(self.templates, self.chicory_api_key,
                                                                   max_tokens=1500, temperature=0.0, model=_MODEL)
            with open(rule_file_name, 'w') as f:
                total_rules = _DIVIDER.join(self.results)
                f.write(total_rules)
        else:
            with open(rule_file_name, 'r') as f:
                total_rules_str = f.read().strip()
                self.results = total_rules_str.split(_DIVIDER)

    def generate_feature_functions(self, dataset):
        parsed_rules = self._parse_rules(self.results, dataset.label_list)
        fct_strs_all = []
        saved_file_name = f'{dataset.data_source}/{dataset.dataset_name}/features/function-{dataset.dataset_name}-{dataset.shot}-{dataset.seed}.out'
        if os.path.isfile(saved_file_name) == False:
            for parsed_rule in tqdm(parsed_rules):
                fct_templates = self.chicory_featureset_agent.get_prompt_for_generating_function(
                    parsed_rule, self.feature_desc
                )
                fct_results = self.chicory_featureset_agent.query_gpt(fct_templates, self.chicory_api_key,
                                                                      max_tokens=1500, temperature=0.0, model=_MODEL)
                fct_strs = [fct_txt.split('<start>')[1].split('<end>')[0].strip() for fct_txt in fct_results]
                fct_strs_all.append(fct_strs)

            with open(saved_file_name, 'w') as f:
                total_str = _VERSION.join([_DIVIDER.join(x) for x in fct_strs_all])
                f.write(total_str)
        else:
            with open(saved_file_name, 'r') as f:
                total_str = f.read().strip()
                fct_strs_all = [x.split(_DIVIDER) for x in total_str.split(_VERSION)]

        return self.validate_feature_functions(fct_strs_all)


    def _parse_rules(self, result_texts, label_list=[]):
        total_rules = []
        splitter = "onditions for class"
        for text in result_texts:
            splitted = text.split(splitter)
            if splitter not in text:
                continue
            if len(label_list) != 0 and len(splitted) != len(label_list) + 1:
                continue

            rule_raws = splitted[1:]
            rule_dict = {}
            for rule_raw in rule_raws:
                class_name = rule_raw.split(":")[0].strip(" .'").strip(' []"')
                rule_parsed = []
                for txt in rule_raw.strip().split("\n")[1:]:
                    if len(txt) < 2:
                        break
                    rule_parsed.append(" ".join(txt.strip().split(" ")[1:]))
                    rule_dict[class_name] = rule_parsed
            total_rules.append(rule_dict)
        return total_rules


    def validate_feature_functions(self, fct_strs_all):
        # Get function names and strings
        fct_names = []
        fct_strs_final = []
        for fct_str_pair in fct_strs_all:
            fct_pair_name = []
            if 'def' not in fct_str_pair[0]:
                continue

            for fct_str in fct_str_pair:
                fct_pair_name.append(fct_str.split('def')[1].split('(')[0].strip())
            fct_names.append(fct_pair_name)
            fct_strs_final.append(fct_str_pair)

        return fct_names, fct_strs_final

    def convert_to_binary_vectors(self, fct_strs_all, fct_names, dataset):
        X_train_all_dict = {}
        X_test_all_dict = {}
        executable_list = []  # Save the parsed functions that are properly working for both train/test sets
        for i in range(len(fct_strs_all)):  # len(fct_strs_all) == # of trials for ensemble
            X_train_dict, X_test_dict = {}, {}
            for label in dataset.label_list:
                X_train_dict[label] = {}
                X_test_dict[label] = {}

            # Match function names with each answer class
            fct_idx_dict = {}
            for idx, name in enumerate(fct_names[i]):
                for label in dataset.label_list:
                    if isinstance(label, str):
                        label_name = '_'.join(label.split(' '))
                    else:
                        label_name = str(label)
                    if label_name.lower() in name.lower():
                        fct_idx_dict[label] = idx

            # If the number of inferred rules are not the same as the number of answer classes, remove the current trial
            if len(fct_idx_dict) != len(dataset.label_list):
                continue

            try:
                for label in dataset.label_list:
                    fct_idx = fct_idx_dict[label]
                    code = fct_strs_all[i][fct_idx].strip('` "')
                    # parsed = ast.parse(code)
                    # check_ast(parsed)
                    logger.debug ("Validating the generated feature function ...")
                    exec(fct_strs_all[i][fct_idx].strip('` "'))
                    X_train_each = locals()[fct_names[i][fct_idx]](dataset.X_train).astype('int').to_numpy()
                    X_test_each = locals()[fct_names[i][fct_idx]](dataset.X_test).astype('int').to_numpy()
                    assert (X_train_each.shape[1] == X_test_each.shape[1])
                    X_train_dict[label] = torch.tensor(X_train_each).float()
                    X_test_dict[label] = torch.tensor(X_test_each).float()

                X_train_all_dict[i] = X_train_dict
                X_test_all_dict[i] = X_test_dict
                executable_list.append(i)
            except Exception as e:  # If error occurred during the function call, remove the current trial
                # logger.error (e)
                continue

        return executable_list, X_train_all_dict, X_test_all_dict

    def predict(self, dataset, executable_list, X_train_all_dict, X_test_all_dict):
        test_outputs_all = []
        multiclass = True if len(dataset.label_list) > 2 else False
        y_train_num = np.array([dataset.label_list.index(k) for k in dataset.y_train])
        y_test_num = np.array([dataset.label_list.index(k) for k in dataset.y_test])

        for i in executable_list:
            X_train_now = np.hstack([X_train_all_dict[i][label].numpy() for label in dataset.label_list])
            X_test_now = np.hstack([X_test_all_dict[i][label].numpy() for label in dataset.label_list])

            # Train
            rfc = self.train_call_back(n_estimators=100, random_state=dataset.seed)
            rfc.fit(X_train_now, y_train_num)

            # Evaluate
            if self.evaluation_metric == 'auc':
                test_outputs = rfc.predict_proba(X_test_now)
            else:
                test_outputs = rfc.predict(X_test_now)

            result_metric = self._evaluate(test_outputs, y_test_num, multiclass=multiclass)
            logger.debug(f"{self.evaluation_metric.upper()}: {result_metric}")

            if self.evaluation_metric == 'auc':
                test_outputs_all.append(test_outputs)
            else:
                test_outputs_all.append(rfc.predict_proba(X_test_now))

        test_outputs_all = np.stack(test_outputs_all, axis=0)

        if self.evaluation_metric == 'auc':
            ensembled_probs = test_outputs_all.mean(0)
        else:
            ensembled_probs = np.argmax(test_outputs_all.mean(0), axis=1)

        return self._evaluate(ensembled_probs, y_test_num, multiclass=multiclass)

    def _evaluate(self, preds, y_true, multiclass):
        if self.evaluation_metric == 'auc':
            if multiclass:
                return roc_auc_score(y_true, preds, multi_class='ovr')
            else:
                return roc_auc_score(y_true, preds[:, 1])
        elif self.evaluation_metric == 'accuracy':
            return accuracy_score(y_true, preds)
