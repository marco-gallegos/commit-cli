from common.functions import get_module_id
from data.modules_repository import IModulesRepository, ModulesRepository, ModuleConfig
from common.constants import constants
from configmanager.config import Configuration

#TODO: with new modules rtepository this looks old fashioned
class ModuleManager(object):
    """
    File format
    """
    modules:list[ModuleConfig]
    repository:IModulesRepository

    def __init__(self, config:Configuration) -> None:
        self.repository = ModulesRepository(config)
        modulesLoaded:list[ModuleConfig] = self.repository.getAll()
        self.modules:list[ModuleConfig] = modulesLoaded


    def update_modules(self, data:ModuleConfig, id:str=None):
        if id is None:
            data.projectid = get_module_id()
        else:
            data.projectid = id
        return self.repository.update(data)


    def get_modules(self) -> list[ModuleConfig]:
        return self.modules


