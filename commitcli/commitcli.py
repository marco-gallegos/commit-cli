import inquirer
import os
#from inquirer.themes import GreenPassion

class CommitMessage(object):
    def __init__(self, format:str="odoo"):
        super()
        self.tag = None
        self.module = None
        self.header = None
        self.body = None
        
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
        return self.questions[self.format]

    
    def get_commit_string(self):
        if self.format == "odoo" or self.format not in self.formats:
            return f"[{self.tag}] {self.module}: {self.header}\n\n{self.body}"


    def set_answers(self, answers:dict):
        self.tag = answers['tag']
        self.module = answers['module']
        self.header = answers['header']
        self.body = answers['body']

    
    def get_answers(self):
        answers = inquirer.prompt(self.questions[self.format])
        self.set_answers(answers)



def main():
    commit_msg = CommitMessage()
    commit_msg.get_answers()
    os.system(f"git commit -m '{commit_msg.get_commit_string()}'")


if __name__ == '__main__':
    main()