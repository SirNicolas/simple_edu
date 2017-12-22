import subprocess
from pathlib import Path


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
        valid, result = subprocess.getstatusoutput("flake8 " + file_path)
        valid = valid is 0
        if not valid:
            errors = result.split('\n')
    else:
        errors = ['File is corrupted']
    return errors, valid
