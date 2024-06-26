import subprocess

from langchain_core.tools import tool


class AWSClient:
    def __call__(self, command, region):
        """
            Runs an AWS CLI command on the shell.

            Args:
                command_str (str): The AWS CLI command to be executed.

            Returns:
                str: The output of the executed command.
            """
        # Add the "aws" prefix to the command
        if "aws" in command:
            full_command = f"{command} --region {region}"
        else:
            full_command = f"aws {command} --region {region}"

        # Run the command on the shell and capture the output
        try:
            output = subprocess.check_output(full_command, shell=True, universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            return None


    def _to_camel_case(case, text):
        """
        Converts a string with words separated by underscores or hyphens to CamelCase.

        Args:
            text (str): The input string to be converted.

        Returns:
            str: The input string converted to CamelCase.
        """
        words = text.split('_')
        camel_case = ''.join(word.capitalize() for word in words)
        return camel_case


    def _parse_parameters(self, params):
        # Converts parameter list into a dictionary
        param_dict = {}
        current_key = None

        for param in params:
            if param.startswith('--'):
                current_key = param.lstrip('--').replace('-', '_')
                current_key = self._to_camel_case(current_key)
                param_dict[current_key] = None
            else:
                if current_key:
                    if param_dict[current_key] is None:
                        param_dict[current_key] = param
                    else:
                        # For parameters that might have multiple values like 'Dimensions'
                        if isinstance(param_dict[current_key], list):
                            param_dict[current_key].append(param)
                        else:
                            param_dict[current_key] = [param_dict[current_key], param]
                current_key = None

        return param_dict


@tool
def aws_client(command, region=None):
    """Get the aws client (boto3) response for passed service/function formatted as a string.
    Also pass the region explicitly for the resource."""
    aws_client = AWSClient()
    if region is not None:
        return aws_client(command, region)
    else:
        regions = ['us-west-1', 'us-west-2', 'us-east-1', 'us-east-2']
        for region in regions:
            svc = aws_client(command, region)
            if svc is not None:
                return svc
        return None
