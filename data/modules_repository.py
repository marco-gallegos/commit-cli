from abc import ABC, abstractmethod

from pymongo.database import Database
import pymongo
from bson.objectid import ObjectId
from common.logger import logger
from configmanager.config import Configuration
from data.db import GetDatabase
import re
import pendulum
from io import TextIOWrapper
import uuid

from typing import List


class ModuleConfig(object):
    id:str
    name:str
    date:int
    last_used:int
    use_count:int
    projectid:str # to filter in formal dbs

    def __init__(self, name:str, date:int = 0, last_used:int = 0, use_count:int = 1, id:str = None, projectid:str = None) -> None:
        self.id:str = id
        self.name:str = name
        self.date:int = date
        self.last_used:int =  last_used
        self.use_count:int = use_count
        self.projectid:str = projectid if projectid is not None else None

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.date} {self.last_used} {self.use_count}"

    def initId(self):
        self.id = uuid.uuid4().hex if self.id is None else self.id

    def get_as_db_row(self):
        return {
            "name": self.name,
            "date": self.date,
            "last_used": self.last_used,
            "use_count": self.use_count,
            "projectid": self.projectid,
        }




# thinked to work as a interface
class IModulesRepository(ABC):
    @abstractmethod
    def getAll(self):
        pass
    
    @abstractmethod
    def get(self, id:str):
        pass

    @abstractmethod
    def update(self, module:ModuleConfig):
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

    def write_db(self, modules_as_csv:str) -> bool:
        # overwrite file
        file = open(self.db, "w")
        file.write(modules_as_csv)
        file.close()
        return True

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
                                content_as_list[1], int(content_as_list[2]),
                                int(content_as_list[3]), int(content_as_list[4]), content_as_list[0]
                            )
                        moduleList.append(module)
                    except:
                        print("error parsing row", content_as_list)
            return moduleList
        return list()

    def get(self, id:str) -> ModuleConfig:
        current_modules:list = self.getAll()
        current_module = [ module for module in current_modules if module.id == id ]
        #TODO: convert to ModuleConfig
        return current_module[0] if len(current_module) > 0 else None 

    
    def update(self, module:ModuleConfig):
        """Update modules file
        1 - get used module
        2 - get modules in file (in this point this module should exist in module manager)
        3 - search for our module inside the result
            3.1 -  if exist update counter and last used
            3.2 - if not exists addit to the list
                a - limit number of modules to write to 10
        4 - save the modules infomation
        """
        current_modules:list[ModuleConfig] = self.getAll()
        new_modules:list[ModuleConfig] = []
        current_date = pendulum.now()
        exist_in_module_list:bool = False
        
        logger.log("INFO", current_modules)

        modules_as_csv:str = ""
        
        if current_modules and len(current_modules) > 0:
            for current_module in current_modules:
                if current_module.id == module.id:
                    current_module.last_used = current_date.int_timestamp
                    current_module.use_count += 1
                    exist_in_module_list = True
                new_modules.append(current_module)
        
        if exist_in_module_list is False:
            new_module:ModuleConfig = ModuleConfig(module.name, current_date.int_timestamp, current_date.int_timestamp, 1)
            new_module.initId()
            new_modules.append(new_module)

        logger.log("INFO", exist_in_module_list)

        new_modules.sort(key=lambda module: module.last_used, reverse=True)

        logger.log("INFO", exist_in_module_list)

        new_modules = new_modules[0:9:1]

        for module in new_modules:
            modules_as_csv += f"{module.id},{module.name},{module.date},{module.last_used},{module.use_count},{module.projectid}\n"

        logger.log("INFO", modules_as_csv)
        
        self.write_db(modules_as_csv)


# ===================================================================

# Assuming you have a ModuleConfig class defined somewhere in your code.
# You can import it here to use it in the class below.

class MongoDbModulesRepository(IModulesRepository):
    def __init__(self, config: Configuration) -> None:
        # super().__init__()
        self.db:Database = GetDatabase(config)
        self.config:Configuration = config
        logger.log("INFO", self.db)

    def getAll(self) -> List[ModuleConfig]:
        modules_collection = self.db["modules"]
        try:
            all_modules = modules_collection.find(
                {
                    "projectid": self.config.config.projectid
                }
            ).sort([("last_used", pymongo.DESCENDING)])
        except:
            all_modules = []

        module_list = []
        for module_doc in all_modules:
            logger.log("INFO", "module ->")
            logger.log("INFO", module_doc)
            try:
                module = ModuleConfig(
                    module_doc["name"],
                    int(module_doc["date"]),
                    int(module_doc["last_used"]),
                    int(module_doc["use_count"]),
                    str(module_doc["_id"])
                )
                module_list.append(module)
            except Exception as e:
                print("Error parsing document:", e)
        return module_list

    def get(self, id:str) -> ModuleConfig:
        pass

    def update(self, module: ModuleConfig):
        modules_collection = self.db["modules"]
        module.use_count += 1
        current_date = pendulum.now()

        module.last_used = current_date.int_timestamp

        if module.id is not None:
            logger.log("INFO", f"updating module -> {module.id}")
            logger.log("INFO", module.get_as_db_row())
            modules_collection.update_one({"_id": ObjectId(module.id)}, {"$set": module.get_as_db_row()})
        else:
            logger.log("INFO", f"creating module {module.name}")
            logger.log("INFO", module.get_as_db_row())
            module.date = current_date.int_timestamp
            module_new = modules_collection.insert_one(module.get_as_db_row())
        return True
# ===================================================================


# repository to expose to the consumers
class ModulesRepository(IModulesRepository):

    def __init__(self, config:Configuration) -> None:
        # super().__init__()
        #TODO: improve this
        if config.config.db == "mongodb":
            self.db = MongoDbModulesRepository(config)
        else:
            self.db = LocalFileDb(config)


    def getAll(self) -> list[ModuleConfig]:
        all = self.db.getAll()
        return all

    def get(self, id:str) -> ModuleConfig:
        return self.db.get(id)

    def update(self, module:ModuleConfig):
        return self.db.update(module)

