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
from common.versions import get_version
from data.modules_repository import ModulesRepository

@click.command()
@click.option('-nop', '--nooptionals', required=False, is_flag=True, help='Do not ask for optional questions')
@click.option('-log', '--onlylog', required=False, is_flag=True, help="Avoid confirmimg the message only make a lopg from the final message" )
@click.option('-v', '--version', required=False, is_flag=True, help="Show the current version" )
def main(nooptionals: bool, onlylog: bool, version: bool) -> bool:
    """Main funtion on this module is implemented to handle a cli call """
    if version is True:
        print(f"version: {get_version()}")
    else:
        do_a_commit(nooptionals, onlylog)
    return True

def get_current_version():
    print(f"current version : {get_version()}")
    return True



def do_a_commit(nooptionals: bool, onlylog: bool) -> bool:
    """Function to make commits, its a wrapper for the 'git commit' command
    this uses the '~/.commitclirc' file to store and manage the config.


    :return: execution status
    :rtype: bool
    """
    forced_config:dict[str, bool] = {
        "avoid_optionals": not nooptionals,
    }
    logger.log("INFO","forced config runing")
    logger.log("INFO", forced_config)
    configuration_manager:ConfigManager = ConfigManager(override_config=forced_config, loadModuleManager=True)
    logger.log("INFO", configuration_manager.config)
    

    #TODO:this is testing replace the actual way to get data
    rep = ModulesRepository(configuration_manager.config)

    modules = rep.getAll()

    if modules:
        for module in modules:
            print(module)

    message_created:bool = create_commit_message(configuration_manager, onlylog)
    return message_created



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
    # print("=="*30)
    

    commit_command:str = f"git commit -m '{commit_string}'"

    if onlylog and onlylog is True:
        print(commit_command)
    else:
        os.system(commit_command)
    
    # update preselected files
    commit_msg.update_preselected_data()

    return True
