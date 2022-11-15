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
from common.logger import logger  

@click.command()
@click.option('-nop', '--nooptionals', required=False, is_flag=True, help='Do not ask for optional questions')
# @click.option(
#    '-f', '--format', required=False, help='Format the commit message',
#    # TODO: this need come from configuration file
#    type=click.Choice([], case_sensitive=False)
# )
@click.option('-log', '--onlylog', required=False, is_flag=True, help="Avoid confirmimg the message only make a lopg from the final message" )
def main(nooptionals: bool, onlylog: bool) -> bool | None:
    """Function to make commits, its a wrapper for the 'git commit' command
    this uses the '~/.commitclirc' file to store and manage the config.

    called by default for this module.

    :return: execution status
    :rtype: bool
    """
    logger.log("INFO", "Hello bby 7u7")
    forced_config:dict[str, bool] = {
        "avoid_optionals": nooptionals,
    }
    configuration_manager:ConfigManager = ConfigManager(override_config=forced_config, loadModuleManager=True)
    create_commit_message(configuration_manager, onlylog)


def create_commit_message(configuration_manager: ConfigManager, onlylog: bool) -> bool:
    commit_msg:CommitMessage = CommitMessage(configuration_manager=configuration_manager)
    are_there_changes:int = os.system("git status --short -uno >> /dev/null")
    if are_there_changes == 32768:
        print("there's not a git repository.")
        return False

    are_there_changes_output:str = os.popen("git diff --name-only --cached").read()  # str with the output
    if len(are_there_changes_output) == 0:
        print("looks like theres no changes to commit.")
        return False

    commit_msg.get_answers()
    commit_string:str|None = commit_msg.get_commit_string()

    if commit_string is None:
        return False

    print("commiting...")
    print("=="*30)
    

    commit_command = f"git commit -m '{commit_string}'"

    if onlylog and onlylog is True:
        print(commit_command)
    else:
        os.system(commit_command)
    
    # update preselected files
    commit_msg.update_preselected_data()

    return True
