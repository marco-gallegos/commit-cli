from abc import ABC, abstractmethod
from common.logger import logger
from configmanager.config import Configuration
from data.db import GetDatabase
import re
import pprint

# new imports
from pymongo import MongoClient
# from bson.objectid import ObjectId
from typing import List



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


# thinked to work as a interface
class IModulesRepository(ABC):
    @abstractmethod
    def getAll(self):
        pass

    @abstractmethod
    def store(self, modules:list[ModuleConfig]):
        pass


# a single db repositpry to serve in ModulesRepository
class LocalFileDb(IModulesRepository):

    def __init__(self, config:Configuration):
        # super().__init__()
        self.db = GetDatabase(config)
        self.regex_clave_valor = r'[\D]+[=]{1}[\w.]+'
        self.pattern_regex_clave_valor = re.compile(self.regex_clave_valor)


        if self.db is None:
            raise Exception("we can not determinate the file DB")
        # logger.log('INFO',self.db)

    def getAll(self) -> List[ModuleConfig]:
        current_file:str = self.db

        if current_file is not None:
            modules_file:TextIOWrapper = open(current_file, "r")
            file_content:list[str] = modules_file.readlines()
            modules_file.close()
            moduleList:list = []

            for content in file_content:
                content_as_list:list[str] = content.replace("\n","").split(",")
                if len(content_as_list) >= 4:
                    # print(content_as_list[0], content_as_list[1], content_as_list[2], content_as_list[3])
                    try:
                        module:ModuleConfig = ModuleConfig(
                                content_as_list[0], int(content_as_list[1]),
                                int(content_as_list[2]), int(content_as_list[3])
                                )
                        moduleList.append(module)
                    except:
                        print("error parsing row", content_as_list)

            return moduleList
        return None

    def store(self, modules: list[ModuleConfig]):
        pass




# ===================================================================

# Assuming you have a ModuleConfig class defined somewhere in your code.
# You can import it here to use it in the class below.

class MongoDbModulesRepository(IModulesRepository):
    def __init__(self, config: Configuration) -> None:
        super().__init__()
        self.db_client = MongoClient(host=config.config.db_url, port=int(config.config.db_port))
        self.db = self.db_client[config.config.db_name]  # Replace 'db_name' with your MongoDB database name
        logger.log("INFO", self.db)

    def getAll(self) -> List[ModuleConfig]:
        modules_collection = self.db["modules"]
        logger.log("INFO", modules_collection)
        all_modules = modules_collection.find()

        logger.log("INFO", all_modules)
        module_list = []
        for module_doc in modules_collection.find():
            logger.log("INFO", "module")
            pprint.pprint(module_doc)
            try:
                module = ModuleConfig(
                    module_doc["name"],
                    int(module_doc["date"]),
                    int(module_doc["last_used"]),
                    int(module_doc["use_count"])
                )
                module_list.append(module)
            except Exception as e:
                print("Error parsing document:", e)
        
        logger.log("INFO","returning")
        return module_list

    def store(self, modules: List[ModuleConfig]):
        modules_collection = self.db["modules"]
        modules_data = []
        for module in modules:
            module_data = {
                "field1": module.field1,
                "field2": module.field2,
                "field3": module.field3,
                "field4": module.field4
            }
            modules_data.append(module_data)

        result = modules_collection.insert_many(modules_data)
        return result.inserted_ids
# ===================================================================


# repository to expose to the consumers
class ModulesRepository(IModulesRepository):
    db:str # or new dbs

    def __init__(self, config:Configuration) -> None:
        super().__init__()

        #TODO: improve this
        if config.config.db == "mongodb":
            self.db_repo = MongoDbModulesRepository(config)
        else:
            self.db_repo = LocalFileDb(config)


    def getAll(self) -> list[ModuleConfig]:
        all = self.db_repo.getAll()
        return all
        

    def store(self):
        pass

