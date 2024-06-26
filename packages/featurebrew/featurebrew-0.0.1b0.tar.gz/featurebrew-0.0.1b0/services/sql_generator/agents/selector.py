from logging import getLogger

from services.sql_generator.agents.base import BaseAgent
from services.sql_generator.const import *
from services.sql_generator.tools.llm import safe_call_llm
from services.sql_generator.utils import *
from typing import List
from copy import deepcopy

import sqlite3
import time
import abc
import sys
import os
import glob
import pandas as pd
from tqdm import tqdm, trange
from pprint import pprint
import pdb
import tiktoken

from services.sql_generator.const import SELECTOR_NAME

# DATA_CHROMA_PATH = os.getenv("DATA_DB_PATH")
# DATA_COLLECTION = os.getenv("DATA_DB_COLLECTION")

PLATFORM_QA_MODEL = os.getenv("PLATFORM_QA_MODEL", "gpt-4o")

data_path = "/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/data"
logger = getLogger(__name__)

class Selector(BaseAgent):
    """
    Get database description and if need, extract relative tables & columns
    """
    name = SELECTOR_NAME
    description = "Get database description and if need, extract relative tables & columns"

    def __init__(self, data_path: str, tables_json_path: str, prompt_template: str, lazy: bool = False,
                 without_selector: bool = False):
        super().__init__()
        # self.data_path = data_path.strip('/').strip('\\')
        self.data_path = data_path.strip('\\')
        self.tables_json_path = tables_json_path
        self.db2infos = {}  # summary of db (stay in the memory during generating prompt)
        self.db2dbjsons = {}  # store all db to tables.json dict by tables_json_path
        self.init_db2jsons()
        if not lazy:
            self._load_all_db_info()
        self._message = {}
        self.without_selector = without_selector
        self.prompt_template = prompt_template

    def init_db2jsons(self):
        if not os.path.exists(self.tables_json_path):
            raise FileNotFoundError(f"tables.json not found in {self.tables_json_path}")
        data = load_json_file(self.tables_json_path)
        for item in data:
            db_id = item['db_id']

            table_names = item['table_names']
            # Number of statistical tables
            item['table_count'] = len(table_names)

            column_count_lst = [0] * len(table_names)
            for tb_idx, col in item['column_names']:
                if tb_idx >= 0:
                    column_count_lst[tb_idx] += 1
            # Maximum number of column names
            item['max_column_count'] = max(column_count_lst)
            item['total_column_count'] = sum(column_count_lst)
            item['avg_column_count'] = sum(column_count_lst) // len(table_names)

            # print()
            # print(f"db_id: {db_id}")
            # print(f"table_count: {item['table_count']}")
            # print(f"max_column_count: {item['max_column_count']}")
            # print(f"total_column_count: {item['total_column_count']}")
            # print(f"avg_column_count: {item['avg_column_count']}")
            # time.sleep(0.2)
            self.db2dbjsons[db_id] = item

    def _get_column_attributes(self, cursor, table, df=None):
        if cursor:
            # Query table column attribute information
            cursor.execute(f"PRAGMA table_info(`{table}`)")
            columns = cursor.fetchall()

            # Construct a dictionary list of column attribute information
            columns_info = []
            primary_keys = []
            column_names = []
            column_types = []
            for column in columns:
                column_names.append(column[1])
                column_types.append(column[2])
                is_pk = bool(column[5])
                if is_pk:
                    primary_keys.append(column[1])
                column_info = {
                    'name': column[1],  # List
                    'type': column[2],  # type of data
                    'not_null': bool(column[3]),  # Whether to allow empty
                    'primary_key': bool(column[5])  # Is it a primary key?
                }
                columns_info.append(column_info)
        elif df is not None:
            # For DataFrame, get column attribute information
            columns_info = []
            primary_keys = []  # Assuming no primary key information in CSV/XLSX
            column_names = df.columns.tolist()
            column_types = [str(df[col].dtype) for col in df.columns]
            for col_name, col_type in zip(column_names, column_types):
                column_info = {
                    'name': col_name,  # List
                    'type': col_type,  # type of data
                    'not_null': not df[col_name].isnull().any(),  # Whether to allow empty
                    'primary_key': False  # Assuming no primary key information
                }
                columns_info.append(column_info)
        else:
            raise ValueError("Either cursor or df must be provided")

        return column_names, column_types

    def _get_unique_column_values_str(self, cursor, table, column_names, column_types,
                                      json_column_names, is_key_column_lst, df=None):

        col_to_values_str_lst = []
        col_to_values_str_dict = {}

        key_col_list = [json_column_names[i] for i, flag in enumerate(is_key_column_lst) if flag]

        len_column_names = len(column_names)

        for idx, column_name in enumerate(column_names):
            # Skip primary keys and foreign keys
            if column_name in key_col_list:
                continue

            lower_column_name = column_name.lower()
            # If the column name ends with id, email, or url, use an empty string
            if lower_column_name.endswith('id') or lower_column_name.endswith('email') or lower_column_name.endswith(
                    'url'):
                values_str = ''
                col_to_values_str_dict[column_name] = values_str
                continue

            if cursor:
                sql = f"SELECT `{column_name}` FROM `{table}` GROUP BY `{column_name}` ORDER BY COUNT(*) DESC"
                cursor.execute(sql)
                values = cursor.fetchall()
                values = [value[0] for value in values]
            else:
                values = df[column_name].dropna().unique().tolist()

            values_str = ''
            # Try to get value examples string, if exception, use an empty string
            try:
                values_str = self._get_value_examples_str(values, column_types[idx])
            except Exception as e:
                logger.error(f"\nerror: get_value_examples_str failed, Exception:\n{e}\n")

            col_to_values_str_dict[column_name] = values_str

        for k, column_name in enumerate(json_column_names):
            values_str = ''
            is_key = is_key_column_lst[k]

            # Primary key or foreign key do not need value string
            if is_key:
                values_str = ''
            elif column_name in col_to_values_str_dict:
                values_str = col_to_values_str_dict[column_name]
            else:
                logger.debug(col_to_values_str_dict)
                time.sleep(3)
                logger.error(f"error: column_name: {column_name} not found in col_to_values_str_dict")

            col_to_values_str_lst.append([column_name, values_str])

        return col_to_values_str_lst

    def _get_value_examples_str(self, values: List[object], col_type: str):
        if not values:
            return ''
        if len(values) > 10 and col_type in ['INTEGER', 'REAL', 'NUMERIC', 'FLOAT', 'INT']:
            return ''

        vals = []
        has_null = False
        for v in values:
            if v is None:
                has_null = True
            else:
                tmp_v = str(v).strip()
                if tmp_v == '':
                    continue
                else:
                    vals.append(v)
        if not vals:
            return ''

        if col_type in ['TEXT', 'VARCHAR']:
            new_values = []
            for v in vals:
                if not isinstance(v, str):
                    new_values.append(v)
                else:
                    v = v.strip()
                    if v == '':  # exclude empty string
                        continue
                    elif ('https://' in v) or ('http://' in v):  # exclude url
                        return ''
                    elif is_email(v):  # exclude email
                        return ''
                    else:
                        new_values.append(v)
            vals = new_values
            tmp_vals = [len(str(a)) for a in vals]
            if not tmp_vals:
                return ''
            max_len = max(tmp_vals)
            if max_len > 50:
                return ''

        if not vals:
            return ''

        vals = vals[:6]

        is_date_column = is_valid_date_column(vals)
        if is_date_column:
            vals = vals[:1]

        if has_null:
            vals.insert(0, None)

        val_str = str(vals)
        return val_str

    def _load_single_db_info(self, db_id: str) -> dict:
        table2coldescription = {}  # Dict {table_name: [(column_name, full_column_name, column_description), ...]}
        table2primary_keys = {}  # DIct {table_name: [primary_key_column_name,...]}

        table_foreign_keys = {}  # Dict {table_name: [(from_col, to_table, to_col), ...]}
        table_unique_column_values = {}  # Dict {table_name: [(column_name, examples_values_str)]}

        db_dict = self.db2dbjsons[db_id]

        # todo: gather all pk and fk id list
        important_key_id_lst = []
        keys = db_dict['primary_keys'] + db_dict['foreign_keys']
        for col_id in keys:
            if isinstance(col_id, list):
                important_key_id_lst.extend(col_id)
            else:
                important_key_id_lst.append(col_id)

        table_names_original_lst = db_dict['table_names_original']
        for tb_idx, tb_name in enumerate(table_names_original_lst):
            # Iterate over original column names
            all_column_names_original_lst = db_dict['column_names_original']

            all_column_names_full_lst = db_dict['column_names']
            col2dec_lst = []

            pure_column_names_original_lst = []
            is_key_column_lst = []
            for col_idx, (root_tb_idx, orig_col_name) in enumerate(all_column_names_original_lst):
                if root_tb_idx != tb_idx:
                    continue
                pure_column_names_original_lst.append(orig_col_name)
                if col_idx in important_key_id_lst:
                    is_key_column_lst.append(True)
                else:
                    is_key_column_lst.append(False)
                full_col_name: str = all_column_names_full_lst[col_idx][1]
                full_col_name = full_col_name.replace('_', ' ')
                cur_desc_obj = [orig_col_name, full_col_name, '']
                col2dec_lst.append(cur_desc_obj)
            table2coldescription[tb_name] = col2dec_lst

            table_foreign_keys[tb_name] = []
            table_unique_column_values[tb_name] = []
            table2primary_keys[tb_name] = []

            if os.path.exists(f"{self.data_path}/{db_id}/{db_id}.sqlite"):
                file_format = 'sqlite'
            elif os.path.exists(f"{self.data_path}/{tb_name}.csv"):
                file_format = 'csv'
            elif os.path.exists(f"{self.data_path}/{tb_name}.xlsx"):
                file_format = 'xlsx'
            else:
                file_format = 'ni'

            if file_format == 'sqlite':
                db_path = f"{self.data_path}/{db_id}/{db_id}.sqlite"
                # db_path = f"{self.data_path}/{db_id}.sqlite"
                logger.debug(f"db_path: {db_path}")
                conn = sqlite3.connect(db_path)
                conn.text_factory = lambda b: b.decode(
                    errors="ignore")  # avoid gbk/utf8 error, copied from sql-eval.exec_eval
                cursor = conn.cursor()
                all_sqlite_column_names_lst, all_sqlite_column_types_lst = self._get_column_attributes(cursor, tb_name)
                col_to_values_str_lst = self._get_unique_column_values_str(cursor, tb_name, all_sqlite_column_names_lst,
                                                                           all_sqlite_column_types_lst,
                                                                           pure_column_names_original_lst,
                                                                           is_key_column_lst)
                if cursor:
                    cursor.close()
            elif file_format == 'csv':
                csv_file = f"{self.data_path}/{tb_name}.csv"
                df = pd.read_csv(csv_file)
                all_sqlite_column_names_lst, all_sqlite_column_types_lst = self._get_column_attributes(None, tb_name, df)
                col_to_values_str_lst = self._get_unique_column_values_str(None, tb_name, all_sqlite_column_names_lst,
                                                                           all_sqlite_column_types_lst,
                                                                           pure_column_names_original_lst,
                                                                           is_key_column_lst, df)
            elif file_format == 'xlsx':
                xlsx_file = f"{self.data_path}/{tb_name}.xlsx"
                df = pd.read_excel(xlsx_file)
                all_sqlite_column_names_lst, all_sqlite_column_types_lst = self._get_column_attributes(None, tb_name,
                                                                                                       df)
                col_to_values_str_lst = self._get_unique_column_values_str(None, tb_name, all_sqlite_column_names_lst,
                                                                           all_sqlite_column_types_lst,
                                                                           pure_column_names_original_lst,
                                                                           is_key_column_lst, df)
            table_unique_column_values[tb_name] = col_to_values_str_lst

        if file_format == 'sqlite':
            foreign_keys_lst = db_dict['foreign_keys']
            for from_col_idx, to_col_idx in foreign_keys_lst:
                from_col_name = all_column_names_original_lst[from_col_idx][1]
                from_tb_idx = all_column_names_original_lst[from_col_idx][0]
                from_tb_name = table_names_original_lst[from_tb_idx]

                to_col_name = all_column_names_original_lst[to_col_idx][1]
                to_tb_idx = all_column_names_original_lst[to_col_idx][0]
                to_tb_name = table_names_original_lst[to_tb_idx]

                table_foreign_keys[from_tb_name].append((from_col_name, to_tb_name, to_col_name))

            for pk_idx in db_dict['primary_keys']:
                pk_idx_lst = []
                if isinstance(pk_idx, int):
                    pk_idx_lst.append(pk_idx)
                elif isinstance(pk_idx, list):
                    pk_idx_lst = pk_idx
                else:
                    err_message = f"pk_idx: {pk_idx} is not int or list"
                    logger.error(err_message)
                    raise Exception(err_message)
                for cur_pk_idx in pk_idx_lst:
                    tb_idx = all_column_names_original_lst[cur_pk_idx][0]
                    col_name = all_column_names_original_lst[cur_pk_idx][1]
                    tb_name = table_names_original_lst[tb_idx]
                    table2primary_keys[tb_name].append(col_name)

        time.sleep(3)

        result = {
            "desc_dict": table2coldescription,
            "value_dict": table_unique_column_values,
            "pk_dict": table2primary_keys,
            "fk_dict": table_foreign_keys
        }
        return result

    def _get_unique_column_values_str_from_df(self, df: pd.DataFrame, column_names: list, is_key_column_lst: list):
        unique_values = []
        for col_name, is_key in zip(column_names, is_key_column_lst):
            if is_key:
                examples_values_str = ', '.join(map(str, df[col_name].unique()[:5]))
                unique_values.append((col_name, examples_values_str))
        return unique_values

    def _load_all_db_info(self):
        logger.info("\nLoading all database info...", file=sys.stdout, flush=True)
        db_ids = [item for item in os.listdir(self.data_path)]
        for i in trange(len(db_ids)):
            db_id = db_ids[i]
            db_info = self._load_single_db_info(db_id)
            self.db2infos[db_id] = db_info

    def _build_bird_table_schema_sqlite_str(self, table_name, new_columns_desc, new_columns_val):
        schema_desc_str = ''
        schema_desc_str += f"CREATE TABLE {table_name}\n"
        extracted_column_infos = []
        for (col_name, full_col_name, col_extra_desc), (_, col_values_str) in zip(new_columns_desc, new_columns_val):
            # district_id INTEGER PRIMARY KEY, -- location of branch
            col_line_text = ''
            col_extra_desc = 'And ' + str(col_extra_desc) if col_extra_desc != '' and str(
                col_extra_desc) != 'nan' else ''
            col_extra_desc = col_extra_desc[:100]
            col_line_text = ''
            col_line_text += f"  {col_name},  --"
            if full_col_name != '':
                full_col_name = full_col_name.strip()
                col_line_text += f" {full_col_name},"
            if col_values_str != '':
                col_line_text += f" Value examples: {col_values_str}."
            if col_extra_desc != '':
                col_line_text += f" {col_extra_desc}"
            extracted_column_infos.append(col_line_text)
        schema_desc_str += '{\n' + '\n'.join(extracted_column_infos) + '\n}' + '\n'
        return schema_desc_str

    def _build_bird_table_schema_list_str(self, table_name, new_columns_desc, new_columns_val):
        schema_desc_str = ''
        schema_desc_str += f"# Table: {table_name}\n"
        # schema_desc_str += f"# Table: {table_name}\n"
        extracted_column_infos = []
        for (col_name, full_col_name, col_extra_desc), (_, col_values_str) in zip(new_columns_desc, new_columns_val):
            col_extra_desc = 'And ' + str(col_extra_desc) if col_extra_desc != '' and str(
                col_extra_desc) != 'nan' else ''
            col_extra_desc = col_extra_desc[:100]

            col_line_text = ''
            col_line_text += f'  ('
            col_line_text += f"{col_name},"

            if full_col_name != '':
                full_col_name = full_col_name.strip()
                col_line_text += f" {full_col_name}."
            if col_values_str != '':
                col_line_text += f" Value examples: {col_values_str}."
            if col_extra_desc != '':
                col_line_text += f" {col_extra_desc}"
            col_line_text += '),'
            extracted_column_infos.append(col_line_text)
        schema_desc_str += '[\n' + '\n'.join(extracted_column_infos).strip(',') + '\n]' + '\n'
        return schema_desc_str

    def _get_db_desc_str(self,
                         db_id: str,
                         extracted_schema: dict,
                         use_gold_schema: bool = False) -> List[str]:
        """
        Add foreign keys, and value descriptions of focused columns.
        :param db_id: name of sqlite database
        :param extracted_schema: {table_name: "keep_all" or "drop_all" or ['col_a', 'col_b']}
        :return: Detailed columns info of db; foreign keys info of db
        """
        if self.db2infos.get(db_id, {}) == {}:  # lazy load
            self.db2infos[db_id] = self._load_single_db_info(db_id)
        db_info = self.db2infos[db_id]
        desc_info = db_info[
            'desc_dict']  # table:str -> columns[(column_name, full_column_name, extra_column_desc): str]
        value_info = db_info['value_dict']  # table:str -> columns[(column_name, value_examples_str): str]
        pk_info = db_info['pk_dict']  # table:str -> primary keys[column_name: str]
        fk_info = db_info['fk_dict']  # table:str -> foreign keys[(column_name, to_table, to_column): str]
        tables_1, tables_2, tables_3 = desc_info.keys(), value_info.keys(), fk_info.keys()
        assert set(tables_1) == set(tables_2)
        assert set(tables_2) == set(tables_3)

        # print(f"desc_info: {desc_info}\n\n")

        # schema_desc_str = f"[db_id]: {db_id}\n"
        schema_desc_str = ''  # for concat
        db_fk_infos = []  # use list type for unique check in db

        # print(f"extracted_schema:\n")
        # pprint(extracted_schema)
        # print()

        logger.debug(f"db_id: {db_id}")
        # For selector recall and compression rate calculation
        chosen_db_schem_dict = {}  # {table_name: ['col_a', 'col_b'], ..}
        for (table_name, columns_desc), (_, columns_val), (_, fk_info), (_, pk_info) in \
                zip(desc_info.items(), value_info.items(), fk_info.items(), pk_info.items()):

            table_decision = extracted_schema.get(table_name, '')
            if table_decision == '' and use_gold_schema:
                continue

            # columns_desc = [(column_name, full_column_name, extra_column_desc): str]
            # columns_val = [(column_name, value_examples_str): str]
            # fk_info = [(column_name, to_table, to_column): str]
            # pk_info = [column_name: str]

            all_columns = [name for name, _, _ in columns_desc]
            primary_key_columns = [name for name in pk_info]
            foreign_key_columns = [name for name, _, _ in fk_info]

            important_keys = primary_key_columns + foreign_key_columns

            new_columns_desc = []
            new_columns_val = []

            logger.debug(f"table_name: {table_name}")
            if table_decision == "drop_all":
                new_columns_desc = deepcopy(columns_desc[:6])
                new_columns_val = deepcopy(columns_val[:6])
            elif table_decision == "keep_all" or table_decision == '':
                new_columns_desc = deepcopy(columns_desc)
                new_columns_val = deepcopy(columns_val)
            else:
                llm_chosen_columns = table_decision
                logger.debug(f"llm_chosen_columns: {llm_chosen_columns}")
                append_col_names = []
                for idx, col in enumerate(all_columns):
                    if col in important_keys:
                        new_columns_desc.append(columns_desc[idx])
                        new_columns_val.append(columns_val[idx])
                        append_col_names.append(col)
                    elif col in llm_chosen_columns:
                        new_columns_desc.append(columns_desc[idx])
                        new_columns_val.append(columns_val[idx])
                        append_col_names.append(col)
                    else:
                        pass

                # todo: check if len(new_columns_val) ≈ 6
                if len(all_columns) > 6 and len(new_columns_val) < 6:
                    for idx, col in enumerate(all_columns):
                        if len(append_col_names) >= 6:
                            break
                        if col not in append_col_names:
                            new_columns_desc.append(columns_desc[idx])
                            new_columns_val.append(columns_val[idx])
                            append_col_names.append(col)

            # Selector
            chosen_db_schem_dict[table_name] = [col_name for col_name, _, _ in new_columns_desc]

            # 1. Build schema part of prompt
            # schema_desc_str += self._build_bird_table_schema_sqlite_str(table_name, new_columns_desc, new_columns_val)
            schema_desc_str += self._build_bird_table_schema_list_str(table_name, new_columns_desc, new_columns_val)

            # 2. Build foreign key part of prompt
            for col_name, to_table, to_col in fk_info:
                from_table = table_name
                if '`' not in str(col_name):
                    col_name = f"`{col_name}`"
                if '`' not in str(to_col):
                    to_col = f"`{to_col}`"
                fk_link_str = f"{from_table}.{col_name} = {to_table}.{to_col}"
                if fk_link_str not in db_fk_infos:
                    db_fk_infos.append(fk_link_str)
        fk_desc_str = '\n'.join(db_fk_infos)
        schema_desc_str = schema_desc_str.strip()
        fk_desc_str = fk_desc_str.strip()

        return schema_desc_str, fk_desc_str, chosen_db_schem_dict

    def _is_need_prune(self, db_id: str, db_schema: str):
        # encoder = tiktoken.get_encoding("cl100k_base")
        # tokens = encoder.encode(db_schema)
        # return len(tokens) >= 25000
        db_dict = self.db2dbjsons[db_id]
        avg_column_count = db_dict['avg_column_count']
        total_column_count = db_dict['total_column_count']
        if avg_column_count <= 6 and total_column_count <= 30:
            return False
        else:
            return True

    def _prune(self,
               db_id: str,
               query: str,
               db_schema: str,
               db_fk: str,
               evidence: str = None,
               ) -> dict:
        prompt = self.prompt_template.format(db_id=db_id, query=query, evidence=evidence, desc_str=db_schema,
                                             fk_str=db_fk)
        word_info = extract_world_info(self._message)
        reply = safe_call_llm(prompt, **word_info)
        extracted_schema_dict = parse_json(reply, True)
        return extracted_schema_dict

    def _concise(self,
                 db_id: str,
                 query: str,
                 db_schema: str,
                 db_fk: str,
                 chosen_db_schem_dict: str,
                 evidence: str = None,
                 ) -> dict:
        prompt = concise_template.format(db_id=db_id, query=query, evidence=evidence, desc_str=db_schema,
                                             fk_str=db_fk, chosen_db_schem_dict=chosen_db_schem_dict)
        word_info = extract_world_info(self._message)
        reply = safe_call_llm(prompt, **word_info)
        extracted_schema_dict = parse_json(reply, False)
        return extracted_schema_dict

    def _features(self,
                 db_id: str,
                 query: str,
                 db_schema: str,
                 db_fk: str,
                 chosen_db_schem_dict: str,
                 evidence: str = None,
                 ) -> dict:
        prompt = features_template.format(db_id=db_id, query=query, evidence=evidence, desc_str=db_schema,
                                             fk_str=db_fk, chosen_db_schem_dict=chosen_db_schem_dict)
        word_info = extract_world_info(self._message)
        reply = safe_call_llm(prompt, **word_info)
        extracted_schema_dict = parse_json(reply, False)
        return extracted_schema_dict

    def talk(self, message: dict):
        """
        :param message: {"db_id": database_name,
                         "query": user_query,
                         "evidence": extra_info,
                         "extracted_schema": None if no preprocessed result found}
        :return: extracted database schema {"desc_str": extracted_db_schema, "fk_str": foreign_keys_of_db}
        """
        if message['send_to'] != self.name: return
        self._message = message
        db_id, ext_sch, query, evidence = message.get('db_id'), \
            message.get('extracted_schema', {}), \
            message.get('query'), \
            message.get('evidence')
        use_gold_schema = False
        if ext_sch:
            use_gold_schema = True
        db_schema, db_fk, chosen_db_schem_dict = self._get_db_desc_str(db_id=db_id, extracted_schema=ext_sch,
                                                                       use_gold_schema=use_gold_schema)
        need_prune = self._is_need_prune(db_id, db_schema)
        if self.without_selector:
            need_prune = False

        if ext_sch == {} and need_prune:
            try:
                try:
                    raw_extracted_schema_dict = self._prune(db_id=db_id, query=query, db_schema=db_schema, db_fk=db_fk,
                                                            evidence=evidence)
                except Exception as e:
                    logger.error(e)
                    raw_extracted_schema_dict = {}

            except Exception as e:
                logger.error(e)
                raw_extracted_schema_dict = {}

            logger.debug(f"query: {message['query']}\n")
            db_schema_str, db_fk, chosen_db_schem_dict = self._get_db_desc_str(db_id=db_id,
                                                                               extracted_schema=raw_extracted_schema_dict)

            message['extracted_schema'] = raw_extracted_schema_dict
            message['chosen_db_schem_dict'] = chosen_db_schem_dict
            message['desc_str'] = db_schema_str
            message['fk_str'] = db_fk
            message['pruned'] = True
            message['send_to'] = SELECTOR_NAME
        else:
            message['chosen_db_schem_dict'] = chosen_db_schem_dict
            message['desc_str'] = db_schema
            message['fk_str'] = db_fk
            message['pruned'] = False
            message['send_to'] = SELECTOR_NAME

        try:
            message['metadata'] = self._concise(db_id=db_id, query=query, db_schema=db_schema, db_fk=db_fk,
                                                chosen_db_schem_dict=chosen_db_schem_dict, evidence=evidence)
        except Exception as e:
            logger.error(e)
            message['metadata'] = {}

        try:
            message['features'] = self._features(db_id=db_id, query=query, db_schema=db_schema, db_fk=db_fk,
                                                chosen_db_schem_dict=chosen_db_schem_dict, evidence=evidence)
        except Exception as e:
            logger.error(e)
            message['features'] = {}

        return message

    def invoke(self, message):
        response = self.talk(message)
        return response


def initialize_selector_agent(data_path,
                              tables_json_path,
                              prompt_template=selector_template,
                              lazy=False):
    data_retriever = Selector(data_path=data_path,
                              tables_json_path=tables_json_path, prompt_template=prompt_template, lazy=lazy)
    return data_retriever


if __name__ == "__main__":
    data_retriever = initialize_selector_agent(data_path="../../../data/datasets/spider/database",
                                               tables_json_path="../../../data/datasets/spider/tables.json")
    message = {
        "db_id": "concert_singer",
        "extracted_schema": {},
        "evidence": "",
        "query": 'How many singers do we have?',
        "send_to": SELECTOR_NAME
    }
    selector_data_chain = data_retriever.invoke(message)
    print(selector_data_chain)
