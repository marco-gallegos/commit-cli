from io import TextIOWrapper
import pathlib
import os


class ModuleConfig(object):
    name:str|None
    date:int|None
    last_used:int
    use_count:int

    def __init__(self, name:str|None = None, date:int = 0, last_used:int = 0, use_count:int = 1) -> None:
        # print("constructing", [name, date, last_used, use_count])
        self.name:str|None = name
        self.date:int|None = date
        self.last_used:int =  last_used
        self.use_count:int = use_count
        # print("finish constructing")


    def __str__(self) -> str:
        return f"{self.name} {self.date} {self.last_used} {self.use_count}"



class ModuleManager(object):
    """
    File format
    """
    _file:str|None


    def __init__(self) -> None:
        self._file:str|None = ".commitcli_modules"
        self.load_modules()


    def current_file(self) -> str | None :
        """this function return the fullpath of the file to store
        the configuration

        :return: string with the full path of the file to
        :rtype: str
        """
        project_file = f"{pathlib.Path.cwd()}/{self._file}"
        return project_file if self.exist_file(project_file) else None


    def exist_file(self, file: str) -> bool:
        """this function returns a boolean value on true if the file
        to store the configuration

        :return: if the file exists on the filesystem
        :rtype: bool
        """
        exist = os.path.exists(file)
        return True if exist else False


    def load_modules(self) -> list[ModuleConfig] | None :
        current_file:str|None = self.current_file()

        if  current_file is not None:
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


    def update_modules(self):
        pass


    def get_modules(self) -> list[ModuleConfig] | None:
        return self.load_modules()



if __name__ == "__main__":
    moduleManager:ModuleManager = ModuleManager()
    # row:ModuleConfig = ModuleConfig("tmti", 10, 9, 1)
    row:ModuleConfig = ModuleConfig()
    print("=="*100)
    #print(row)
    #print(moduleManager.get_modules())

