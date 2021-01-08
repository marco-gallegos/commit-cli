"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    
"""
import os, pathlib
from configmanager.config import Configuration
import re, distutils.util


class ConfigManager(object):
    """

    Args:
        object ([type]): [description]
    """
    def __init__(self, file:str='.commitclirc', config:Configuration=None):
        self._file = file
        self.config = config
        self.regex_clave_valor = r'[\D]+[=]{1}[\w]+'
        self.pattern_regex_clave_valor = re.compile(self.regex_clave_valor)
        self.init_config()

    def current_file(self):
        return f"{pathlib.Path.home()}/{self._file}"
    

    def exist_file(self)->bool:
        exist = os.path.exists(self.current_file())
        return True if exist else False

    def stringline_to_key_value(self, string_line:str="#comentario")->str:
        key, value = None, None
        match = re.fullmatch(self.pattern_regex_clave_valor, string_line)
        if match and type(string_line) == str:
            elements = string_line.split("=")
            key= elements[0]
            value= elements[1]
        return key,value

    def load_file(self):
        if self.exist_file():
            data_dict = {}
            file= open(self.current_file(), 'r')
            file_text=file.readlines()
            file.close()
            for file_line in file_text:
                file_line = file_line.replace('\n', '')
                key, value = self.stringline_to_key_value(string_line=file_line)
                if value == "False" or value == "True" or value == "false" or value == "true":
                    value = bool(distutils.util.strtobool(value.lower()))
                data_dict[key] = value
            return data_dict

    
    def save_file(self):
        pass


    def init_config(self)->bool:
        if self.exist_file():
            data = self.load_file()
            print(data)
            self.config = Configuration(config=data)
            return True
        else:
            self.config = Configuration()
            self.save_file()
            return False