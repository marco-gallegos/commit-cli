from io import TextIOWrapper
import pathlib
import os
from data.modules_repository import ModulesRepository


class ModuleConfig(object):
    name:str
    date:int
    last_used:int
    use_count:int

    def __init__(self, name:str = None, date:int = 0, last_used:int = 0, use_count:int = 1) -> None:
        # print("constructing", [name, date, last_used, use_count])
        self.name:str = name
        self.date:int = date
        self.last_used:int =  last_used
        self.use_count:int = use_count
        # print("finish constructing")


    def __str__(self) -> str:
        return f"{self.name} {self.date} {self.last_used} {self.use_count}"



class ModuleManager(object):
    """
    File format
    """
    _file:str
    modules:list[ModuleConfig]


    def __init__(self, config) -> None:
        self._file:str = ".ignore.commitcli_modules"
        
        modulesRepository = ModulesRepository(config)
        modulesLoaded = modulesRepository.getAll()
        self.modules:list[ModuleConfig] = modulesLoaded


    def update_modules(self):
        pass


    def get_modules(self) -> list[ModuleConfig]:

        return self.modules


