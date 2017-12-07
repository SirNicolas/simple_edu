import subprocess


def check_code(file):
    process = subprocess.Popen(["flake8", file.path], stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8')
