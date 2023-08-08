from data.modules_repository import IModulesRepository, ModulesRepository, ModuleConfig
from common.constants import constants

#TODO: with new modules rtepository this looks old fashioned
class ModuleManager(object):
    """
    File format
    """
    modules:list[ModuleConfig]
    repository:IModulesRepository

    def __init__(self, config) -> None:
        self.repository = ModulesRepository(config)
        modulesLoaded:list[ModuleConfig] = self.repository.getAll()
        self.modules:list[ModuleConfig] = modulesLoaded


    def update_modules(self):
        return self.repository


    def get_modules(self) -> list[ModuleConfig]:
        return self.modules


