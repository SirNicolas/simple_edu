import inspect
from enum import Enum
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


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices
