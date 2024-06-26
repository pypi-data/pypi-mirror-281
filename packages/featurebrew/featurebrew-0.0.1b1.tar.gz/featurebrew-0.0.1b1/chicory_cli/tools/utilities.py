import click
import os
import subprocess
import shlex
import yaml

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


def run_shell_command(command, print=False):
    logger.debug ("Running Command: '{}'".format(command))
    cmd = shlex.split(command)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(process.stdout.readline, b''):
        if print:
            click.echo(line)
    process.stdout.close()
    process.wait()
    return process.returncode

def run_shell_command_and_forget(command):
    logger.debug ("Running Command: '{}'".format(command))
    cmd = shlex.split(command)
    process = subprocess.Popen(cmd, bufsize=1)
    process.wait()

def run_shell_command_with_response(command):
    logger.debug ("Running Command: '{}'".format(command))
    cmd = shlex.split(command)
    process = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def get_base_classifier(class_path: str):
    import importlib
    # Split the string to get the module path and the class name
    module_name, class_name = class_path.rsplit('.', 1)
    # Import the module
    module = importlib.import_module(module_name)
    # Get the class
    cls = getattr(module, class_name)
    # Ensure cls is a class type
    if not isinstance(cls, type):
        raise TypeError(f"{class_name} is not a class.")
    logger.debug (f"Identified classifier: {cls}")
    return cls



