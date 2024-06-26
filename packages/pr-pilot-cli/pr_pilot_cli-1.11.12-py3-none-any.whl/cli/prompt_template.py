import os
import subprocess

import click
import jinja2
from pr_pilot.util import create_task
from rich.prompt import Prompt

from cli.task_handler import TaskHandler

MAX_RECURSION_LEVEL = 3


def sh(shell_command, status):
    """Run a shell command and return the output"""
    status.start()
    status.update(f"Running shell command: {shell_command}")
    if isinstance(shell_command, str):
        shell_command = shell_command.split()
    subprocess_params = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(shell_command, **subprocess_params)
    if result.stderr:
        status.fail()
    else:
        status.success(start_again=False)
    status.stop()
    return result.stdout + result.stderr


def read_env_var(variable, default=None):
    """Get the value of an environment variable, with a default value."""
    if variable not in os.environ and default is None:
        # Ask for Variable input with click
        os.environ[variable] = Prompt.ask(f"Enter value for {variable}")
    return os.environ.get(variable, default)


def wrap_function_with_status(func, status):
    def wrapper(*args, **kwargs):
        kwargs["status"] = status
        return func(*args, **kwargs)

    return wrapper


class PromptTemplate:

    def __init__(self, template_file_path, repo, model, status, recursion_level=0, **kwargs):
        self.template_file_path = template_file_path
        self.repo = repo
        self.model = model
        self.status = status
        self.variables = kwargs
        self.recursion_level = recursion_level

    def render(self):

        def subtask(prompt, status, **kwargs):
            # Treat prompt as a file path and read the content if the file exists
            # The file name will be relative to the current jinja template
            full_template_path = os.path.join(os.getcwd(), self.template_file_path)
            current_template_path = os.path.dirname(full_template_path)
            potential_file_path = os.path.join(current_template_path, prompt)
            status.start()
            if os.path.exists(potential_file_path):

                if self.recursion_level >= MAX_RECURSION_LEVEL:
                    status.update(f"Abort loading {prompt}. Maximum recursion level reached.")
                    status.fail()
                    return ""
                sub_template = PromptTemplate(
                    potential_file_path,
                    self.repo,
                    self.model,
                    status,
                    self.recursion_level - 1,
                    **kwargs,
                )
                prompt = sub_template.render()

            try:
                status.update("Creating sub-task ...")
                task = create_task(self.repo, prompt, log=False, gpt_model=self.model)
                task_handler = TaskHandler(task, status)
                return task_handler.wait_for_result(verbose=False, print_result=False)
            except Exception as e:
                raise click.ClickException(f"Error creating sub-task: {e}")
            finally:
                status.stop()

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
        env.globals.update(env=read_env_var)
        env.globals.update(subtask=wrap_function_with_status(subtask, self.status))
        env.globals.update(sh=wrap_function_with_status(sh, self.status))
        template = env.get_template(self.template_file_path)
        return template.render(self.variables)
