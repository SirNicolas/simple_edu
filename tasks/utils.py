from flake8.api import legacy as flake8
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
        style_guide = flake8.get_style_guide(ignore=['E24', 'W503'])
        report = style_guide.check_files([file_path])
        errors = report.get_statistics('')
        valid = len(errors) == 0

    return errors, valid
