"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    The config manager is a class to manage the configuration file by default in ~/.commitclirc
"""
import distutils.util
import os
import pathlib
import re

from loguru import logger

from configmanager.config import Configuration


class ConfigManager(object):
    # data
    # moduleManager:ModuleManager|None

    def __init__(
            self, file: str = '.commitclirc',
            config: Configuration = None,
            override_config:dict = None,
        ) -> None:

        self._file:str = file
        self.config:Configuration = config
        self.regex_clave_valor = r'[\D]+[=]{1}[\w.]+'
        self.pattern_regex_clave_valor = re.compile(self.regex_clave_valor)

        # some initial starts
        self.init_config(override_config=override_config)


    def current_file(self) -> str:
        """this function return the fullpath of the file to store
        the configuration

        :return: string with the full path of the file to
        :rtype: str
        """
        global_file = f"{pathlib.Path.home()}/{self._file}"
        project_file = f"{pathlib.Path.cwd()}/{self._file}"
        return project_file if self.exist_file(project_file) else global_file


    def exist_file(self, file: str) -> bool:
        """this function returns a boolean value on true if the file
        to store the configuration

        :return: if the file exists on the filesystem
        :rtype: bool
        """
        exist = os.path.exists(file)
        return True if exist else False


    def stringline_to_key_value(self, string_line: str = "#comentario") -> tuple[str, str]:
        """This functions returns the separated values by '=' of a string in 
        format 'some=other'

        :param string_line: a string in fomat 'some=other', defaults to "#comentario"
        :type string_line: str, optional
        :return: the values on left and right side of the '=' character
        :rtype: str, str
        """
        key, value = None, None
        match = re.fullmatch(self.pattern_regex_clave_valor, string_line)
        if match and type(string_line) == str and string_line:
            elements = string_line.split("=")
            key= elements[0]
            value= elements[1]
            logger.info(key, value)
        return key, value


    def load_file(self, file: str) -> dict:
        """Method to convert the configuration file into a dictionary

        :return: dictionary with al the key value files in thee file
        :rtype: dict
        """
        current_file = file
        if self.exist_file(current_file):
            data_dict = {}
            file_read = open(current_file, 'r')
            file_text = file_read.readlines()
            file_read.close()
            for file_line in file_text:
                file_line = file_line.replace('\n', '')
                key, value = self.stringline_to_key_value(string_line=file_line)
                if value == "False" or value == "True" or value == "false" or value == "true":
                    value = bool(distutils.util.strtobool(value.lower()))
                if key is not None and value is not None:
                    data_dict[key] = value
            return data_dict
        else:
            return None

    def save_file(self) -> bool:
        """Method to save the current configuration into the configured file

        :return: True
        :rtype: bool
        """
        file = open(self.current_file(), 'w')
        file.write(self.config.get_configuration_file_string())
        file.close()
        return True


    def init_config(self, force_reload: bool = False, override_config: dict = None) -> bool:
        """Method to initialize the class, triggering the load of the file or load
        creating a defaul config and save it on the file.

        :return: boolean representing the previous existence of the config file
        :rtype: bool
        """
        if self.config is None:
            current_file = self.current_file()
            if self.exist_file(current_file):
                data = self.load_file(current_file)
                self.config = Configuration(config=data, override_config=override_config)
                return True
            else:
                self.config = Configuration(override_config=override_config)
                self.save_file()
                return False
        return False 

    def get_config(self, name: str) -> str or bool or None:
        if self.config is not None and self.config.config is not None and self.config.config[name] is not None:
            return self.config.config[name]
        else:
            return None

