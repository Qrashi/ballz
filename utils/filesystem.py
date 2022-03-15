"""
Utilities to interact with the file system
"""
from os import path, stat, makedirs
from typing import TextIO


def abs_filename(file: str) -> str:
    """
    Get the absolute filename of a string (/home/user/path/to/file)
    :param file: filepath to get absolute path of
    :return: absolute filepath
    """
    return path.abspath(file)


def generate(file: str, default: str = "{}"):
    """
    Check if a file exists and create it if nonexistent
    :param file: filepath to file
    :param default: Default to save in case file is nonexistent
    :return:
    """
    if path.exists(file):
        if not stat(file).st_size < len(default.encode('utf-8')):
            return
    else:
        makedirs(path.dirname(file), exist_ok = True)
    with open(file, "w+") as file:
        file.write(default)


def load(file: str, mode: str = "r", default: str = "{}") -> TextIO:
    """
    Get a TextIO to write to a file, will create file if nonexistent
    :param file: Path to file to open
    :param mode: mode to open with ("r"/"w")
    :param default: Default file contents (if file is nonexistent)
    :return: TextIO to write to (with load("example.text", "r") as file:
    """
    generate(file, default)
    return open(file, mode)
