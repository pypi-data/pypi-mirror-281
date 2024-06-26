import os

from sql_generator.agents.decomposer import Decomposer
from sql_generator.agents.refiner import Refiner
from sql_generator.agents.selector import Selector
from sql_generator.const import SYSTEM_NAME, SELECTOR_NAME, MAX_ROUND

import time
from pprint import pprint


class ChatManager(object):
    def __init__(self, data_path: str, tables_json_path: str, log_path: str,lazy: bool=False, without_selector: bool=False):
        self.data_path = data_path  # root path to database dir, including all databases
        self.tables_json_path = tables_json_path # path to table description json file
        self.log_path = log_path  # path to record important printed content during running
        # self.ping_network()
        self.chat_group = [
            Selector(data_path=self.data_path, tables_json_path=self.tables_json_path, lazy=lazy, without_selector=without_selector),
            Decomposer(),
            Refiner(data_path=self.data_path)
        ]

    def _chat_single_round(self, message: dict):
        # we use `dict` type so value can be changed in the function
        for agent in self.chat_group:  # check each agent in the group
            if message['send_to'] == agent.name:
                agent.talk(message)

    def start(self, user_message: dict):
        # we use `dict` type so value can be changed in the function
        start_time = time.time()
        if user_message['send_to'] == SYSTEM_NAME:  # in the first round, pass message to prune
            user_message['send_to'] = SELECTOR_NAME
        for _ in range(MAX_ROUND):  # start chat in group
            self._chat_single_round(user_message)
            if user_message['send_to'] == SYSTEM_NAME:  # should terminate chat
                break
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\033[0;34mExecute {exec_time} seconds\033[0m", flush=True)


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv("../../../resources/.env")

    db_path = os.getenv('DS_PATH')
    test_manager = ChatManager(data_path=f"../../../data/datasets/spider/database",
                               log_path="",
                               tables_json_path=f"../../../data/datasets/spider/tables.json",
                               lazy=True)
    # msg = {
    #     'db_id': 'concert_singer',
    #     'query': 'How many singers do we have?',
    #     'evidence': '',
    #     'extracted_schema': {},
    #     'ground_truth': 'SELECT count(*) FROM singer',
    #     'difficulty': 'easy',
    #     'send_to': SYSTEM_NAME
    # }
    msg = {
        "db_id": "course_teach",
        "extracted_schema": {},
        "evidence": "",
        "query": 'Show the name of the teacher for the math course.',
        "send_to": SYSTEM_NAME
    }
    test_manager.start(msg)
    pprint(msg)
    print(msg['pred'])