import sqlite3

from sql_generator.agents.base import BaseAgent
from sql_generator.const import SYSTEM_NAME, REFINER_NAME, refiner_template
from func_timeout import func_set_timeout, FunctionTimedOut

from sql_generator.tools.llm import safe_call_llm
from sql_generator.utils import add_prefix, extract_world_info, parse_sql_from_string


class Refiner(BaseAgent):
    name = REFINER_NAME
    description = "Execute SQL and preform validation"

    def __init__(self, data_path: str):
        super().__init__()
        self.data_path = data_path  # path to all databases
        self._message = {}

    @func_set_timeout(120)
    def _execute_sql(self, sql: str, db_id: str) -> dict:
        # Get database connection
        db_path = f"{self.data_path}/{db_id}/{db_id}.sqlite"
        conn = sqlite3.connect(db_path)
        conn.text_factory = lambda b: b.decode(errors="ignore")
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            return {
                "sql": str(sql),
                "data": result[:5],
                "sqlite_error": "",
                "exception_class": ""
            }
        except sqlite3.Error as er:
            return {
                "sql": str(sql),
                "sqlite_error": str(' '.join(er.args)),
                "exception_class": str(er.__class__)
            }
        except Exception as e:
            return {
                "sql": str(sql),
                "sqlite_error": str(e.args),
                "exception_class": str(type(e).__name__)
            }

    def _is_need_refine(self, exec_result: dict):
        # spider exist dirty values, even gold sql execution result is None
        if 'data' not in exec_result:
            return True
        return False

        data = exec_result.get('data', None)
        if data is not None:
            if len(data) == 0:
                exec_result['sqlite_error'] = 'no data selected'
                return True
            for t in data:
                for n in t:
                    if n is None:  # fixme fixme fixme fixme fixme
                        exec_result['sqlite_error'] = 'exist None value, you can add `NOT NULL` in SQL'
                        return True
            return False
        else:
            return True

    def _refine(self,
                query: str,
                evidence: str,
                schema_info: str,
                fk_info: str,
                error_info: dict) -> dict:

        sql_arg = add_prefix(error_info.get('sql'))
        sqlite_error = error_info.get('sqlite_error')
        exception_class = error_info.get('exception_class')
        prompt = refiner_template.format(query=query, evidence=evidence, desc_str=schema_info, \
                                         fk_str=fk_info, sql=sql_arg, sqlite_error=sqlite_error, \
                                         exception_class=exception_class)

        word_info = extract_world_info(self._message)
        reply = safe_call_llm(prompt, **word_info)
        res = parse_sql_from_string(reply)
        return res

    def talk(self, message: dict):
        """
        Execute SQL and preform validation
        :param message: {"query": user_query,
                        "evidence": extra_info,
                        "desc_str": description of db schema,
                        "fk_str": foreign keys of database,
                        "final_sql": generated SQL to be verified,
                        "db_id": database name to execute on}
        :return: execution result and if need, refine SQL according to error info
        """
        if message['send_to'] != self.name: return
        self._message = message
        db_id, old_sql, query, evidence, schema_info, fk_info = message.get('db_id'), \
            message.get('pred', message.get('final_sql')), \
            message.get('query'), \
            message.get('evidence'), \
            message.get('desc_str'), \
            message.get('fk_str')
        # do not fix sql containing "error" string
        if 'error' in old_sql:
            message['try_times'] = message.get('try_times', 0) + 1
            message['pred'] = old_sql
            message['send_to'] = SYSTEM_NAME
            return

        is_timeout = False
        try:
            error_info = self._execute_sql(old_sql, db_id)
        except Exception as e:
            is_timeout = True
        except FunctionTimedOut as fto:
            is_timeout = True

        is_need = self._is_need_refine(error_info)
        # is_need = False
        if not is_need or is_timeout:  # correct in one pass or refine success or timeout
            message['try_times'] = message.get('try_times', 0) + 1
            message['pred'] = old_sql
            message['send_to'] = SYSTEM_NAME
        else:
            new_sql = self._refine(query, evidence, schema_info, fk_info, error_info)
            message['try_times'] = message.get('try_times', 0) + 1
            message['pred'] = new_sql
            message['fixed'] = True
            message['send_to'] = REFINER_NAME

        return message

    def invoke(self, message):
        response = self.talk(message)
        return response


def initialize_refiner_agent(data_path):
    data_retriever = Refiner(data_path)
    return data_retriever


if __name__ == "__main__":
    data_retriever = initialize_refiner_agent(data_path="../../../data/datasets/spider/database")
    message = {}
    refiner_data_chain = data_retriever.invoke(message, 'How many singers do we have?')
    print(refiner_data_chain)
