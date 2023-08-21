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
from configmanager.format_module_manager import ModuleManager
from data.modules_repository import ModuleConfig
import pendulum


@click.command()
@click.option('-nop', '--nooptionals', required=False, is_flag=True, help='Do not ask for optional questions')
@click.option('-log', '--onlylog', required=False, is_flag=True, help="Avoid confirmimg the message only make a lopg from the final message" )
@click.option('-v', '--version', required=False, is_flag=True, help="Show the current version" )
def main(nooptionals: bool, onlylog: bool, version: bool) -> bool:
    """Main funtion on this module is implemented to handle a cli call """
    if version is True:
        get_current_version()
    else:
        do_a_commit(nooptionals, onlylog)
    return True


def get_current_version():
    print(f"current version : {get_version()}")
    return True


def validate_current_repository() -> bool:
    """Validate that we can make a commit"""
    are_there_changes:int = os.system("git status --short -uno >> /dev/null")
    if are_there_changes == 32768:
        print("there's not a git repository.")
        return False

    are_there_changes_output:str = os.popen("git diff --name-only --cached").read()  # str with the output
    if len(are_there_changes_output) == 0:
        print("looks like theres no changes to commit.")
        return False
    return True


def do_a_commit(nooptionals: bool, onlylog: bool) -> bool:
    """Function to make commits, its a wrapper for the 'git commit' command
    this uses the '~/.commitclirc' file to store and manage the config.


    :return: execution status
    :rtype: bool
    """
    can_commit = validate_current_repository()
    if (can_commit is not True):
        return False
    
    forced_config:dict[str, bool] = {
        "avoid_optionals": not nooptionals,
    }
    logger.log("INFO","forced config runing")
    logger.log("INFO", forced_config)

    configuration_manager:ConfigManager = ConfigManager(override_config=forced_config)

    logger.log("INFO", configuration_manager.config)

    module_manager = ModuleManager(configuration_manager.config)   

    commit:CommitMessage|None = None
    commit = create_commit_message(configuration_manager, module_manager, onlylog)
    
    if commit is not None:
        new_module:ModuleConfig
        current_date = pendulum.now()
        if commit.moduleid is not None:
            stored_module:ModuleConfig = module_manager.get(commit.moduleid)
            new_module = ModuleConfig(commit.module, stored_module.date, current_date.int_timestamp, stored_module.use_count, commit.moduleid, configuration_manager.config.config.projectid)
        else:
            new_module = ModuleConfig(commit.module, 0, 0, 0, commit.moduleid, configuration_manager.config.config.projectid)

        logger.log("INFO", "=========================>")
        logger.log("INFO", new_module)
        module_manager.update_modules(new_module, new_module.id)

    return True if commit is not None else False


def create_commit_message(configuration_manager: ConfigManager, module_manager:ModuleManager, onlylog: bool) -> CommitMessage:
    commit_msg:CommitMessage = CommitMessage(configuration_manager=configuration_manager, module_manager=module_manager)

    commit_string:str = None
    
    try:
        commit_msg.get_answers()
    except KeyboardInterrupt:
        #BUG: this doesnt works
        print("cancelling commit.")
    except Exception:
        print("Cancelling commit.")

    logger.log("INFO", commit_msg)

    commit_string = commit_msg.get_commit_string()

    logger.log("INFO", commit_string)

    if commit_string is None:
        return None

    print("commiting...")

    commit_command:str = f"git commit -m '{commit_string}'"

    if onlylog and onlylog is True:
        print(commit_command)
    else:
        os.system(commit_command)

    return commit_msg

