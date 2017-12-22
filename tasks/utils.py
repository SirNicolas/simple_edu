import subprocess


def check_code(file):
    without_errors, result = subprocess.getstatusoutput("flake8 " + file.path)
    without_errors = bool(without_errors)
    if without_errors:
        result = result.split('\n')
    return result, without_errors
