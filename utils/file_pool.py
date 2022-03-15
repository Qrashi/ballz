"""FilePool provides a general location for all open jsonFiles"""
import sys
from typing import Dict

from .filesystem import abs_filename
from .json_file import JsonFile

if __name__ == "__main__":
    print("The file pool is only meant to be imported!")
    sys.exit()


class FilePool:
    """
    FilePool holds all currently used JsonFiles
    """

    __pool: Dict[str, JsonFile] = {}

    def open(self, filepath: str, default: str = "{}") -> JsonFile:
        """
        Open a .json file from the filesystem
        :param filepath: The path to the .json file
        :param default: Default to save if file is nonexistent invalid syntax
        :return: A JsonFile object
        """
        filepath = abs_filename(filepath)
        if filepath not in self.__pool:
            self.__pool[filepath] = JsonFile(filepath, default=default)
        return self.__pool[filepath]

    def sync(self):
        """
        Save all files to the filesystem
        :return:
        """
        for file in self.__pool.values():
            file.save()
        print("✓ Files saved!")
