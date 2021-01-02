"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    This file contains a class to abstract a commit message
"""
import inquirer, os

class CommitMessage(object):
    """This clas is a abstraction of a commit message,
    this class must to generate a formatted commit string

    Args:
        object (object): base object from python
    """
    
    def __init__(self, 
        format:str="odoo", 
        tag:str=None, 
        module:str=None, 
        header:str=None, 
        body:str=None, 
    ):
        """Constructor of the class to

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
        
        self.format = format

        self.formats = [
            "odoo"
        ]

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
        }


    def get_questions(self):
        """Method to return the current questions of

        Returns:
            list: list with the questions
        """
        return self.questions[self.format]

    
    def get_commit_string(self):
        """Method to return the formathed commit string

        Returns:
            str: formatted commit string
        """
        if self.can_generate_string():
            if self.format == "odoo" or self.format not in self.formats:
                return f"[{self.tag}] {self.module}: {self.header}\n\n{self.body}"
        else:
            print("no se puede generar commit")
        return None


    def set_answers(self, answers:dict):
        """Method to set the answers from the user

        Args:
            answers (dict): answers provided by the user
        """
        if answers:
            self.tag = answers['tag']
            self.module = answers['module']
            self.header = answers['header']
            self.body = answers['body']

    
    def get_answers(self):
        """Method to get the answers from the user
        """
        answers = inquirer.prompt(self.questions[self.format])
        if answers:
            self.set_answers(answers)

    def can_generate_string(self):
        """Method to determinate if we can build the commit message
        for the selected format

        Returns:
            bool: true if we can build the string
        """
        if self.format == "odoo":
            return self.tag and self.module and self.header and self.body
        else:
            return False