from __future__ import annotations #to make it work on 3.9 or lower

from pymongo import MongoClient
from pymongo.database import Database
from configmanager.config import Configuration
from common.constants import constants
import pygit2
import os
# from common.logger import logger


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


def returnFileDb() -> str:
    '''This return the full file path'''
    project_file:str = get_git_root()
    file_name = constants['db']['filename']
    
    if project_file is not None:
        project_file:str = f"{project_file}{file_name}"

        if os.path.exists(project_file) is False:
            file = open(project_file, "a")
            file.close()

    return project_file


def MongoDb(config:Configuration) -> Database:
    '''This return the full file path'''
    try:
        db_client:MongoClient = MongoClient(host=config.config.db_url, port=int(config.config.db_port), timeoutMS=0, connect=True)
        db:Database = db_client[config.config.db_name]
    except Exception as e:
        db = None
        print("could not connect mongodb")
    return db


def GetDatabase (config:Configuration) -> (None|str|Database):
    if config.config["db"] == "localfile":
        return returnFileDb()
    if config.config["db"] == "mongodb":
        return MongoDb(config)


    return None
