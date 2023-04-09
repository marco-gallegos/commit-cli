from abc import ABC, abstractmethod


class ModuleConfig(object):
    name:str
    date:int
    last_used:int
    use_count:int

    def __init__(self, name:str, date:int = 0, last_used:int = 0, use_count:int = 1) -> None:
        # print("constructing", [name, date, last_used, use_count])
        self.name:str = name
        self.date:int = date
        self.last_used:int =  last_used
        self.use_count:int = use_count
        # print("finish constructing")


    def __str__(self) -> str:
        return f"{self.name} {self.date} {self.last_used} {self.use_count}"


# thjinked to work as a interface
class IModulesRepository(ABC):
    @abstractmethod
    def getAll(self):
        pass

    @abstractmethod
    def store(self, modules:list[ModuleConfig]):
        pass


# a single db repositpry to serve in ModulesRepository
class LocalFileDb(IModulesRepository):
    def getAll(self):
        pass



# repository to expose to the consumers
class ModulesRepository(IModulesRepository):

    def __init__(self) -> None:
        super().__init__()

    def getAll(self):
        pass

