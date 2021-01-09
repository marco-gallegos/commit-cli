"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    This file conatains a function to build a commit message using a
    terminal menu
"""
import os
from commitcli.commit_message import CommitMessage
from configmanager.config_manager import ConfigManager


def main()->bool:
    """Funcion para realizar el commit

    :return: estado de la ejecucion
    :rtype: bool
    """
    commit_msg = CommitMessage()
    are_there_changes = os.system("git status --short -uno >> /dev/null")
    if are_there_changes == 32768:
        print("no existe un repositorio git")
        return False

    are_there_changes_output = os.popen("git diff --name-only --cached").read() #str with the output
    if len(are_there_changes_output) == 0:
        print("no hay cambios por ser rastreados")
        return False
    
    commit_msg.get_answers()
    commit_string = commit_msg.get_commit_string()

    if commit_string:
        print("haciendo commit")
        print("=="*30)
        os.system(f"git commit -m '{commit_string}'")
    
    return True