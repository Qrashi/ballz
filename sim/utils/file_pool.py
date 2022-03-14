from typing import Dict

from .filesystem import abs_filename
from .json_file import JsonFile

if __name__ == "__main__":
    print("The file pool is only meant to be imported!")
    exit()


class FilePool:
    def __init__(self):
        self.__pool: Dict[str, JsonFile] = {}

    def open(self, filepath: str, default: str = "{}") -> JsonFile:
        filepath = abs_filename(filepath)
        if filepath not in self.__pool:
            self.__pool[filepath] = JsonFile(filepath, default=default)
        return self.__pool[filepath]

    def sync(self):
        for file in self.__pool.values():
            file.save()
        print("✓ Files saved!")


pool = FilePool()
