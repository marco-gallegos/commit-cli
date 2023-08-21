import pygit2
import os
from common.logger import logger

def get_git_root():
    try:
        repo = pygit2.Repository('.')
    # for now catch any error is good enough
    except:
        return None
    
    git_root = repo.workdir
    if git_root is not None and os.path.isdir(git_root):
        return git_root
    else:
        return None

def get_first_commit_id(repo_path:str):
    # Abrir el repositorio
    repo = pygit2.Repository(repo_path)

    # Obtener el primer commit
    first_commit = next(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL))

    # Devolver el ID del primer commit como un string hexadecimal
    return first_commit.id.hex


def get_project_id() -> str:
    repo_path = get_git_root()
    logger.log("INFO", repo_path)
    first_commit:str = get_first_commit_id(repo_path)
    logger.log("INFO", first_commit)
    return f"{first_commit}"

