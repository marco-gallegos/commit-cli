from configmanager.config import Configuration
from common.constants import constants
import pygit2
import os
from common.logger import logger

def get_git_root():
    try:
        repo = pygit2.Repository('.')
    except:
        return None
    
    git_root = repo.workdir
    if git_root is not None and os.path.isdir(git_root):
        return git_root
    else:
        return None

def exist_file(file: str) -> bool:
        """this function returns a boolean value on true if the file
        to store the configuration

        :return: if the file exists on the filesystem
        :rtype: bool
        """
        exist = os.path.exists(file)
        return True if exist else False


def returnFileDb(filename:str = " nt") -> str|None:
    '''This return the full file path'''
    project_file = get_git_root()
    file_name = constants['db']['filename']
    
    if project_file is not None:
        project_file = f"{project_file}{file_name}"

    return project_file



def GetDatabase (config:Configuration) -> str|None:
    if config.config["db"] == constants["config_names"]["db"]["file"]:
        return returnFileDb()

    return None
