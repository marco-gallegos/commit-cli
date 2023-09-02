from data.modules_repository import IModulesRepository, ModulesRepository, ModuleConfig
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
        try:
            self.modules:list[ModuleConfig] = self.repository.getAll()
        except:
            self.modules = []

    def update_modules(self, data:ModuleConfig, id:str=None):
        return self.repository.update(data)


    def get_modules(self) -> list[ModuleConfig]:
        return self.modules

    def get(self, id:str) -> ModuleConfig:
        modules_matching = [ module for module in self.modules if module.id == id ]
        return modules_matching[0]


