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
@click.option('-nop', '--nooptionals', required=False, is_flag=True, help='Do not ask for optional questions')
# @click.option(
#    '-f', '--format', required=False, help='Format the commit message',
#    # TODO: this need come from configuration file
#    type=click.Choice([], case_sensitive=False)
# )
def main(nooptionals: bool) -> bool:
    """Function to make commits, its a wrapper for the 'git commit' command
    this uses the '~/.commitclirc' file to store and manage the config.

    called by default for this module.

    :return: execution status
    :rtype: bool
    """
    forced_config = {
        "avoid_optionals": nooptionals,
    }
    configuration_manager = ConfigManager(override_config=forced_config)
    create_commit_message(configuration_manager)


def create_commit_message(configuration_manager: ConfigManager) -> bool:
    commit_msg = CommitMessage(configuration_manager=configuration_manager)
    are_there_changes = os.system("git status --short -uno >> /dev/null")
    if are_there_changes == 32768:
        print("there's not a git repository.")
        return False

    are_there_changes_output = os.popen("git diff --name-only --cached").read()  # str with the output
    if len(are_there_changes_output) == 0:
        print("looks like theres no changes to commit.")
        return False

    commit_msg.get_answers()
    commit_string = commit_msg.get_commit_string()

    if commit_string:
        print("commiting...")
        print("=="*30)
        os.system(f"git commit -m '{commit_string}'")
        # print(commit_string)
        # print("done :)")

    return True
