from io import TextIOWrapper
import pathlib
import os

class ModuleManager(object):
    """
    File format
    """
    _file:str

    def __init__(self) -> None:
        self._file = ".commitcli_modules"

    def current_file(self) -> str | None :
        """this function return the fullpath of the file to store
        the configuration

        :return: string with the full path of the file to
        :rtype: str
        """
        project_file = f"{pathlib.Path.cwd()}/{self._file}"
        return project_file if self.exist_file(project_file) else None


    def exist_file(self, file: str) -> bool:
        """this function returns a boolean value on true if the file
        to store the configuration

        :return: if the file exists on the filesystem
        :rtype: bool
        """
        exist = os.path.exists(file)
        return True if exist else False

    def load_modules(self):
        current_file:str = self.current_file()

        if  current_file is not None:
            modules_file:TextIOWrapper = open(current_file, "r")
            file_content:list[str] = modules_file.readlines()

    def update_modules(self):
        pass


    def get_modules(self):
        pass


