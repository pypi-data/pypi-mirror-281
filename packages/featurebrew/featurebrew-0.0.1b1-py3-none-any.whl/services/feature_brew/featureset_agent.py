import random
import openai
import time
import json
import numpy as np
from tqdm import tqdm

# from torch.testing._internal.distributed.rpc.examples.reinforcement_learning_rpc_test import Agent

RULE_PROMPT_TEMPLATE = """
You are an expert. Given the task description and the list of features and data examples, you are extracting conditions for each answer class to solve the task.

Task: [TASK]

Features:
[FEATURES]

Examples:
[EXAMPLES]

Let's first understand the problem and solve the problem step by step.

Step 1. Analyze the causal relationship or tendency between each feature and task description based on general knowledge and common sense within a short sentence. 

Step 2. Based on the above examples and Step 1's results, infer 10 different conditions per answer, following the format below. The condition should make sense, well match examples, and must match the format for [condition] according to value type.

Format for Response:
[FORMAT]


Format for [Condition]:
For the categorical variable only,
- [Feature_name] is in [list of Categorical_values]
For the numerical variable only,
- [Feature_name] (> or >= or < or <=) [Numerical_value]
- [Feature_name] is within range of [Numerical_range_start, Numerical_range_end]


Answer: 
Step 1. The relationship between each feature and the task description: 
"""

FUNCTION_PROMPT_TEMPLATE = """
Provide me a python code for function, given description below.

Function name: [NAME]

Input: Dataframe df_input

Input Features:
[FEATURES]

Output: Dataframe df_output. Create a new dataframe df_output. Each column in df_output refers whether the selected column in df_input follows the condition (1) or not (0). Be sure that the function code well matches with its feature type (i.e., numerical, categorical).

Conditions: 
[CONDITIONS]


Wrap only the function part with <start> and <end>, and do not add any comments, descriptions, and package importing lines in the code.
"""

# class FeatureSetAgent(Agent):
class FeatureSetAgent():

    def get_prompt_for_asking(self, dataset, default_target_attribute, meta_file_name, task_desc, num_query=5):
        try:
            with open(meta_file_name, "r") as f:
                meta_data = json.load(f)
        except:
            meta_data = {}

        print ("Fetching datatset info:\n")
        print(meta_data)

        task_desc = f"{task_desc}\n"
        df_incontext = dataset.X_train.copy()
        df_incontext[default_target_attribute] = dataset.y_train

        format_list = [f'10 different conditions for class "{label}":\n- [Condition]\n...' for label in dataset.label_list]
        format_desc = '\n\n'.join(format_list)

        template_list = []
        current_query_num = 0
        end_flag = False
        while True:
            if current_query_num >= num_query:
                break

            # Feature bagging
            if len(df_incontext.columns) >= 20:
                total_column_list = []
                for i in range(len(df_incontext.columns) // 10):
                    column_list = df_incontext.columns.tolist()[:-1]
                    random.shuffle(column_list)
                    total_column_list.append(column_list[i * 10:(i + 1) * 10])
            else:
                total_column_list = [df_incontext.columns.tolist()[:-1]]

            for selected_column in total_column_list:
                if current_query_num >= num_query:
                    break

                # Sample bagging
                threshold = 16
                if len(df_incontext) > threshold:
                    sample_num = int(threshold / df_incontext[default_target_attribute].nunique())
                    df_incontext = df_incontext.groupby(
                        default_target_attribute, group_keys=False
                    ).apply(lambda x: x.sample(sample_num))

                feature_name_list = []
                sel_cat_idx = [df_incontext.columns.tolist().index(col_name) for col_name in selected_column]
                is_cat_sel = np.array(dataset.is_cat)[sel_cat_idx]

                for cidx, cname in enumerate(selected_column):
                    if is_cat_sel[cidx] == True:
                        clist = dataset.X_all[cname].unique().tolist()
                        if len(clist) > 20:
                            clist_str = f"{clist[0]}, {clist[1]}, ..., {clist[-1]}"
                        else:
                            clist_str = ", ".join(clist)
                        desc = meta_data[cname] if cname in meta_data.keys() else ""
                        feature_name_list.append(
                            f"- {cname}: {desc} (categorical variable with categories [{clist_str}])")
                    else:
                        desc = meta_data[cname] if cname in meta_data.keys() else ""
                        feature_name_list.append(f"- {cname}: {desc} (numerical variable)")

                feature_desc = "\n".join(feature_name_list)

                in_context_desc = ""
                df_current = df_incontext.copy()
                df_current = df_current.groupby(
                    default_target_attribute, group_keys=False
                ).apply(lambda x: x.sample(frac=1))

                for icl_idx, icl_row in df_current.iterrows():
                    answer = icl_row[default_target_attribute]
                    icl_row = icl_row.drop(labels=default_target_attribute)
                    icl_row = icl_row[selected_column]
                    in_context_desc += self._serialize(icl_row)
                    in_context_desc += f"\nAnswer: {answer}\n"

                fill_in_dict = {
                    "[TASK]": task_desc,
                    "[EXAMPLES]": in_context_desc,
                    "[FEATURES]": feature_desc,
                    "[FORMAT]": format_desc
                }
                template = self._fill_in_templates(fill_in_dict, RULE_PROMPT_TEMPLATE)
                template_list.append(template)
                current_query_num += 1

        return template_list, feature_desc


    def _serialize(self, row):
        target_str = f""
        for attr_idx, attr_name in enumerate(list(row.index)):
            if attr_idx < len(list(row.index)) - 1:
                target_str += " is ".join([attr_name, str(row[attr_name]).strip(" .'").strip('"').strip()])
                target_str += ". "
            else:
                if len(attr_name.strip()) < 2:
                    continue
                target_str += " is ".join([attr_name, str(row[attr_name]).strip(" .'").strip('"').strip()])
                target_str += "."
        return target_str


    def _fill_in_templates(self, fill_in_dict, template_str):
        for key, value in fill_in_dict.items():
            if key in template_str:
                template_str = template_str.replace(key, value)
        return template_str


    def query_gpt(self, text_list, api_key, max_tokens=30, temperature=0.0, max_try_num=10, model="gpt-4-turbo"):
        openai.api_key = api_key
        result_list = []
        for prompt in tqdm(text_list):
            curr_try_num = 0
            while curr_try_num < max_try_num:
                # messages = [
                #     {
                #         "role": "system",
                #         "content": "You are an expert datascientist assistant solving ML use-cases. You answer only by generating code. Answer as concisely as possible.",
                #     },
                #     {"role": "user", "content": prompt}],
                try:
                    response = openai.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "user", "content": prompt}],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=1
                    )
                    result = response.choices[0].message.content
                    result_list.append(result)
                    # from langchain.llms import OpenAI
                    #
                    # llm = OpenAI(model_name=model, temperature=temperature, max_tokens=max_tokens, top_p=1)
                    #
                    # result = llm(prompt)
                    # result_list.append(result)
                    break
                except openai._exceptions.BadRequestError as e:
                    return [-1]
                except Exception as e:
                    print(e)
                    curr_try_num += 1
                    if curr_try_num >= max_try_num:
                        result_list.append(-1)
                    time.sleep(10)
        return result_list

    def get_prompt_for_generating_function(self, parsed_rule, feature_desc):
        template_list = []
        for class_id, each_rule in parsed_rule.items():
            function_name = f'extracting_features_{class_id}'
            rule_str = '\n'.join([f'- {k}' for k in each_rule])

            fill_in_dict = {
                "[NAME]": function_name,
                "[CONDITIONS]": rule_str,
                "[FEATURES]": feature_desc
            }
            template = self._fill_in_templates(fill_in_dict, FUNCTION_PROMPT_TEMPLATE)
            template_list.append(template)

        return template_list