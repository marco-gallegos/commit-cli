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
import click


@click.command()
def main() -> bool:
    """Function to make commits, its a wrapper for the 'git commit' command
    this uses the '~/.commitclirc' file to store and manage the config

    :return: execution status
    :rtype: bool
    """
    configuration = ConfigManager()
    commit_msg = CommitMessage(configuration_manager=configuration)
    are_there_changes = os.system("git status --short -uno >> /dev/null")
    if are_there_changes == 32768:
        print("there's not a git repository here")
        return False

    are_there_changes_output = os.popen("git diff --name-only --cached").read()  # str with the output
    if len(are_there_changes_output) == 0:
        print("no hay cambios por ser rastreados")
        return False
    
    commit_msg.get_answers()
    commit_string = commit_msg.get_commit_string()

    if commit_string:
        print("commiting...")
        print("=="*30)
        os.system(f"git commit -m '{commit_string}'")
    
    return True