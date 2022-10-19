"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    This file contains a class to abstract a commit message
"""
import inquirer
from commitcli.common import changes_choices_by_format, get_questions

from configmanager.config_manager import ConfigManager


class CommitMessage(object):
    """This clas is a abstraction of a commit message,
    this class must to generate a formatted commit string

    Args:
        object (object): base object from python
    """
    
    def __init__(
        self,
        format: str = "cc",
        configuration_manager: ConfigManager = ConfigManager(),
        tag: str|None = None,
        module: str|None = None,
        header: str|None = None,
        body: str|None = None,
        footer: str|None = None,
    ):
        """Constructor of the class

        Args:
            format (str, optional): format to use. Defaults to "odoo".
            tag (str, optional): tag for the commit string. Defaults to None.
            module (str, optional): module affected for the commit string. Defaults to None.
            header (str, optional): header for the commit string. Defaults to None.
            body (str, optional): body for the commit string. Defaults to None.
        """
        super()
        self.tag = tag
        self.module = module
        self.header = header
        self.body = body
        self.footer = footer
        self.config:ConfigManager = configuration_manager
        
        self.format = self.config.config.config['format']

        self.choices:dict[str,list[tuple]] = changes_choices_by_format


    def get_commit_string(self)->str|None:
        """Method to return the formathed commit string

        Returns:
            str: formatted commit string
        """
        if self.can_generate_string():
            if self.format == "odoo" or self.format not in self.config.config.supported_formats:
                return f"[{self.tag}] {self.module}: {self.header}\n\n{self.body}"
            elif self.format == "free":
                return f"{self.body}"
            elif self.format == "cc":
                return "{tag}{module}: {header}{body}{footer}".format(
                    tag=self.tag,
                    module= ( "" if not self.module else f"({self.module})"),
                    header= self.header,
                    body= ( "" if not self.body else f"\n\n{self.body}"),
                    footer= ( "" if not self.footer else f"\n\n{self.footer}"),
                )
            else:
                print("error creating commit string")
        else:
            print("we can not create commit")
        return None


    def set_answers(self, answers:dict):
        """Method to set the answers from the user

        Args:
            answers (dict): answers provided by the user
        """
        if answers:
            if self.format == 'odoo':
                self.tag = answers['tag']
                self.module = answers['module']
                self.header = answers['header']
                self.body = answers['body']
            elif self.format == 'free':
                self.body = answers['body']
            elif self.format == 'sgc':
                pass
            elif self.format == 'cc':
                self.tag = answers['tag']
                self.module = answers['module']
                self.header = answers['header']
                if 'body' in answers:
                    self.body = answers['body']
                if 'footer' in answers:
                    self.footer = answers['footer']
            return True
        else:
            return False


    def get_preselected_answers(self) -> dict[str,str]:
        """check for possible preselected answers according the current format"""
        preselected_answers:dict[str,str]
        # TODO: doing

        return preselected_answers


    def get_answers(self):
        """Method to get the answers from the user
        1 - check for preselections
        2 - request filtered answers
        3 - set up all answers
        """
        preselected_answers:dict = self.get_easy_answers()
        answers:dict[str,str] = inquirer.prompt(self.questions[self.format])
        if answers:
            # if self.format in self.optional_questions and not self.config.get_config("avoid_optionals"):
                # for question in self.optional_questions[self.format]:
                    # set_question = input(f"set the {question.name} (y,*): ")
                    # if set_question.lower() == 'y':
                        # temp_dict = inquirer.prompt({question})
                        # answers.update(temp_dict)
            self.set_answers(answers)


    def can_generate_string(self) -> bool:
        """Method to determinate if we can build the commit message
        for the selected format

        Returns:
            bool: true if we can build the string
        """
        if self.format == "odoo":
            return self.tag and self.module and self.header and self.body
        elif self.format == "free":
            return self.body
        elif self.format == "sgc":
            return False
        elif self.format == "cc":
            return self.tag and self.header
        else:
            return False
