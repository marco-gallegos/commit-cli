"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    This file contains a class to abstract a commit message
"""
import inquirer, os
from configmanager.config_manager import ConfigManager


class CommitMessage(object):
    """This clas is a abstraction of a commit message,
    this class must to generate a formatted commit string

    Args:
        object (object): base object from python
    """
    
    def __init__(
        self,
        format: str = "odoo",
        configuration_manager: ConfigManager = ConfigManager(),
        tag: str = None,
        module: str = None,
        header: str = None,
        body: str = None,
        footer: str = None,
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
        self.config = configuration_manager
        
        # probablemente se deba quitar
        self.format = self.config.config.config['format']

        self.choices = {
            "odoo": [
                (
                    "IMP: for improvements: most of the changes done in development version are incremental improvements not related to another tag",
                    "IMP"
                ),
                (
                    "FIX: for bug fixes: mostly used in stable version but also valid if you are fixing a recent bug in development version",
                    "FIX"
                ),
                (
                    "ADD: for adding new modules",
                    "ADD"
                ),
                (
                    "REM: for removing resources: removing dead code, removing views, removing modules, …",
                    "REM"
                ),
                (
                    "REF: for refactoring: when a feature is heavily rewritten",
                    "REF"
                ),
                (
                    "MOV: for moving files: use git move and do not change content of moved file otherwise Git may loose track and history of the file; also used when moving code from one file to another",
                    "MOV"
                ),
                (
                    "REV for reverting commits: if a commit causes issues or is not wanted reverting it is done using this tag",
                    "REV"
                ),
            ],
            "free":[

            ],
            "sgc":[

            ],
            "cc":[
                (
                    'build : Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)',
                    'build'
                ),
                (
                    'ci : Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)',
                    'ci'
                ),
                (
                    'chore : Updates and changes',
                    'chore'
                ),
                (
                    'docs : Documentation only changes',
                    'docs'
                ),
                (
                    'feat : A new feature',
                    'feat'
                ),
                (
                    'fix : A bug fix',
                    'fix'
                ),
                (
                    'perf : A code change that improves performance',
                    'perf'
                ),
                (
                    'refactor : A code change that neither fixes a bug nor adds a feature',
                    'refactor'
                ),
                (
                    'revert: revert of the code',
                    'revert'
                ),
                (
                    'style : Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)',
                    'style'
                ),
                (
                    'test : Adding missing tests or correcting existing tests',
                    'test'
                ),

            ]
        }

        self.questions = {
            "odoo": [
                inquirer.List(name='tag', message='select the type of tag', choices=self.choices[self.format] ),
                inquirer.Text(name='module', message="module name", validate=lambda _, x: x != '.'),
                inquirer.Text(name='header', message="header message", validate=lambda _, x: x != '.'),
                inquirer.Editor(name='body', message='body of the commit'),
                #inquirer.Confirm(name='correct',  message="tag: {tag}, module: {module} , header: {header} \n {body}\nContinue?", default=False),
            ],
            "sgc":[
            ],
            "cc":[
                inquirer.List(name='tag', message='select the type', choices=self.choices[self.format] ),
                inquirer.Text(name='module', message="scope", validate=lambda _, x: x != '.'),
                inquirer.Text(name='header', message="description", validate=lambda _, x: x != '.'),
            ],
            "free":[
                inquirer.Editor(name='body', message='body of the commit'),
            ]
        }

        self.optional_questions = {
            "cc":[
                inquirer.Editor(name='body', message='body of the commit'),
                inquirer.Editor(name='footer', message='footer of the commit'),
            ]
        }

    def get_questions(self, optionals:bool=False):
        """Method to return the current questions of

        Returns:
            list: list with the questions
        """
        if optionals:
            return self.optional_questions[self.format]
        else:
            return self.questions[self.format]
    
    def get_commit_string(self)->str:
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

    def get_answers(self):
        """Method to get the answers from the user
        """
        answers = inquirer.prompt(self.questions[self.format])
        if answers:
            if self.format in self.optional_questions and not self.config.get_config("avoid_optionals"):
                for question in self.optional_questions[self.format]:
                    set_question = input(f"set the {question.name} (y,*): ")
                    if set_question.lower() == 'y':
                        temp_dict = inquirer.prompt({question})
                        answers.update(temp_dict)
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