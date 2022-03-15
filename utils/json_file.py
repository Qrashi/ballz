"""
A JsonFile defines a .json object on the disk
"""
import json
from typing import Union

from .filesystem import abs_filename, load


class JsonFile:

    """
    An object describing a .json file in storage
    """
    __filename: str  # Filename on disk, not accessible
    json: Union[dict, list]  # json as python dictionary or list

    def __init__(self, filename: str, default: str = "{}"):
        """
        Create a new JsonFile object and load the json from memory
        :param filename: filename to load json from
        :param default: default if loading fails
        """
        self.__filename = abs_filename(filename)
        json_file = load(self.__filename, default=default)
        self.json: dict = json.load(json_file)
        json_file.close()

    def reload(self):
        """
        Reload the json file (override contents with content from disk)
        :return:
        """
        with load(self.__filename) as json_file:
            self.json = json.load(json_file)

    def save(self):
        """
        Save the contents of the python dictionary to the disk
        :return:
        """
        with load(self.__filename, mode="w") as json_file:
            json.dump(self.json, json_file, indent=4, sort_keys=True)
