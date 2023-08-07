from io import TextIOWrapper
import pathlib
import os
from data.modules_repository import ModulesRepository, ModuleConfig


#TODO: with new modules rtepository this looks old fashioned
class ModuleManager(object):
    """
    File format
    """
    _file:str
    modules:list[ModuleConfig]


    def __init__(self, config) -> None:
        self._file:str = ".ignore.commitcli_modules"
        
        modulesRepository = ModulesRepository(config)
        modulesLoaded:list[ModuleConfig] = modulesRepository.getAll()
        self.modules:list[ModuleConfig] = modulesLoaded


    def update_modules(self):
        pass


    def get_modules(self) -> list[ModuleConfig]:
        return self.modules


