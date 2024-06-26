import click
import logging
import openai_multi_tool_use_parallel_patch  # import applies the patch
import openai

# Suppress specific warning message
class UserAgentFilter(logging.Filter):
    def filter(self, record):
        return 'USER_AGENT environment variable not set' not in record.getMessage()


# Custom filter class
class SelectiveFilter(logging.Filter):
    def filter(self, record):
        # Only allow messages containing "ALLOWED" to pass through
        return "ALLOWED" in record.getMessage()


# Custom filter class to suppress specific warning messages
class LangChainDeprecationFilter(logging.Filter):
    def filter(self, record):
        # Suppress messages containing 'LangChainDeprecationWarning'
        return 'LangChainDeprecationWarning' not in record.getMessage()

# Get the root logger
logger = logging.getLogger()

# Add the filter
logger.addFilter(UserAgentFilter())
logger.addFilter(LangChainDeprecationFilter())

# Set the logging level for httpx to WARNING to suppress INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)
# Set to the lowest level to capture all messages
logger.setLevel(logging.INFO)

@click.group(help="[Experimental] CLI tool to access Chicory autopilot data engineer")
def main():
    driver = create_clidriver()
    rc = driver.main()
    return rc


from chicory_cli.commands import create, prepare, feature

# Adding commands logic
main.add_command(create.create)
main.add_command(prepare.prepare)
main.add_command(feature.feature)


def create_clidriver():
    # define session
    driver = CLIDriver()
    return driver


class CLIDriver(object):

    def __init__(self):
        pass

    def main(self, args=None):
        """
        """
        # if args is None:
        #     args = sys.argv[1:]
        #
        return 0