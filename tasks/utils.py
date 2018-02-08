import json
import subprocess
import tempfile
from io import FileIO
from pathlib import Path
from typing import List

from autograder_sandbox import AutograderSandbox
from flake8.api import legacy as flake8

from .models import Task


class CompletedCommand:
    def __init__(self, return_code: int, stdout: FileIO, stderr: FileIO,
                 timed_out: bool,
                 stdout_truncated: bool, stderr_truncated: bool):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.timed_out = timed_out
        self.stdout_truncated = stdout_truncated
        self.stderr_truncated = stderr_truncated


class Sandbox(AutograderSandbox):

    def run_command(self,
                    args: List[str],
                    max_num_processes: int=None,
                    max_stack_size: int=None,
                    max_virtual_memory: int=None,
                    as_root: bool=False,
                    stdin: FileIO=None,
                    timeout: int=None,
                    check: bool=False,
                    truncate_stdout: int=None,
                    truncate_stderr: int=None,
                    input: str=None) -> 'CompletedCommand':
        cmd = ['docker', 'exec', '-i', self.name, 'cmd_runner.py']

        if timeout is not None:
            cmd += ['--timeout', str(timeout)]

        cmd += args

        with tempfile.TemporaryFile() as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE,
                               check=True, input=input, encoding='ascii')
                f.seek(0)
                json_len = int(f.readline().decode().rstrip())
                results_json = json.loads(f.read(json_len).decode())

                stdout_len = int(f.readline().decode().rstrip())
                stdout = tempfile.NamedTemporaryFile()
                stdout.write(f.read(stdout_len))
                stdout.seek(0)

                stderr_len = int(f.readline().decode().rstrip())
                stderr = tempfile.NamedTemporaryFile()
                stderr.write(f.read(stderr_len))
                stderr.seek(0)

                result = CompletedCommand(return_code=results_json['return_code'],
                                          timed_out=results_json['timed_out'],
                                          stdout=stdout,
                                          stderr=stderr,
                                          stdout_truncated=results_json['stdout_truncated'],
                                          stderr_truncated=results_json['stderr_truncated'])

                if (result.return_code != 0 or results_json['timed_out']) and check:
                    raise subprocess.CalledProcessError(
                        result.return_code, cmd,
                        output=result.stdout, stderr=result.stderr)

                return result
            except subprocess.CalledProcessError as e:
                f.seek(0)
                print(f.read())
                print(e.stderr)
                raise


def check_code(file_path):
    """
    Basic code check with flake8
    :param file_path:
    :return: errors list and bool(valid/invalid)
    """
    valid = False
    errors = []
    if all([Path(file_path).exists(), Path(file_path).is_file(),
            file_path.endswith('.py')]):
        style_guide = flake8.get_style_guide(ignore=['E24', 'W503'])
        report = style_guide.check_files([file_path])
        errors = report.get_statistics('')
        valid = len(errors) == 0

    return errors, valid


def test_code(task_id):
    """
    Testing code in docker container
    :param task_id: Task id
    :return: list of errors and valid/invalid
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return ['Code file does not exist'], False
    else:
        # our docker sandbox
        with Sandbox() as sandbox:
            for case in task.cases.all():
                ss = ''
                for item in case.get_input_items():
                    ss += '{}\n'.format(item.value)
                sandbox.add_files(task.file.file.name)
                code_output = sandbox.run_command(['python', task.file.name],
                                                  timeout=100, input=ss)
                code_errors = code_output.stderr.read().decode()
                # TODO необходимо привести в порядок вывод ошибок и
                # результатов тестирования кода
                if code_errors:
                    print(code_errors)
                else:
                    code_output = code_output.stdout.read().decode()
                    test_output = []
                    for item in case.get_output_items():
                        test_output.append(item.value)
                    print(code_output, test_output)
    return [], True
