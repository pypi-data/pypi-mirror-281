import os
import subprocess
from typing import Annotated, Any
from langchain_core.tools import tool


class LocalClient:
    def __init__(self):
        self.env = os.environ.copy()

    def run_command(self, command: Annotated[str, "Command line command to be run locally"]) -> list[tuple[Any, ...]]:
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True, env=self.env)
            if result.stdout:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            print(e)
            return str(e)


@tool
def cli_client(command):
    """Get the local process client (subprocess) response for command formatted as a string."""
    local_client = LocalClient()
    return local_client(command)