import inquirer
from configmanager.format_module_manager import ModuleManager, ModuleConfig

class PreselectedQuestion(object):

    def __init__(self, name:str, get_function) -> None:
        self.name:str = name
        self.get_value = get_function

def get_preselected_module(moduleManager:ModuleManager) -> list[ModuleConfig] | None:
    print("calling this function")
    return moduleManager.get_modules()

changes_choices_by_format:dict[str,list[tuple]] = {
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

def get_preselected_questions(format:str)-> list[PreselectedQuestion]:
    question_list:list[PreselectedQuestion] = []

    preselected_questions_by_format:dict[str,dict] = {
        "cc": {
            "module": PreselectedQuestion("module", get_preselected_module)
        }
    }

    questions_to_search:dict[str,dict] = preselected_questions_by_format

    if format in questions_to_search:
        format_questions = questions_to_search[format]
        for question_to_make in format_questions:
            question_list.append(format_questions[question_to_make])

    return question_list

def get_questions(format:str, already_know_answers:list[str], optionals:bool = False) -> dict[str, list]:
    questions:list = []

    questions_by_format:dict[str,dict] ={
        "odoo": {
            "tag":      inquirer.List(name='tag', message='select the type of tag', choices=changes_choices_by_format[format] ),
            "module":   inquirer.Text(name='module', message="module name", validate=lambda _, x: x != '.'),
            "header":   inquirer.Text(name='header', message="header message", validate=lambda _, x: x != '.'),
            "body":     inquirer.Editor(name='body', message='body of the commit'),
            #inquirer.Confirm(name='correct',  message="tag: {tag}, module: {module} , header: {header} \n {body}\nContinue?", default=False),
        },
        "sgc":{
        },
        "cc":{
            "tag":      inquirer.List(name='tag', message='select the type', choices=changes_choices_by_format[format] ),
            "module":   inquirer.Text(name='module', message="scope", validate=lambda _, x: x != '.'),
            "header":   inquirer.Text(name='header', message="description", validate=lambda _, x: x != '.'),
        },
        "free":{
            "body":     inquirer.Editor(name='body', message='body of the commit'),
        }
    }

    optional_questions_by_format:dict[str, dict] = {
        "cc":{
            "body":     inquirer.Editor(name='body', message='body of the commit'),
            "footer":   inquirer.Editor(name='footer', message='footer of the commit'),
        }
    }

    questions_to_search:dict[str,dict] = questions_by_format if optionals is False else optional_questions_by_format

    if format in questions_to_search:
        format_questions = questions_to_search[format]
        for question_to_make in format_questions:
            if question_to_make not in already_know_answers:
                questions.append(format_questions[question_to_make])
    
    print("questions to make",{f"{format}": questions})

    return {f"{format}": questions}
