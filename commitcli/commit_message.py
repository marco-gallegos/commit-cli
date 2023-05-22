"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    This file contains a class to abstract a commit message
"""
import inquirer
from configmanager.format_module_manager import ModuleManager
from commitcli.common import changes_choices_by_format, get_questions, get_preselected_questions, PreselectedQuestion

from configmanager.config_manager import ConfigManager
from configmanager.format_module_manager import ModuleConfig
import pendulum

class CommitMessage(object):
    """This clas is a abstraction of a commit message,
    this class must to generate a formatted commit string

    Args:
        object (object): base object from python
    """
    
    def __init__(
        self,
        # format: str = "cc",
        module_manager: ModuleManager,
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
        self.config:ConfigManager = configuration_manager
        self.module_manager:ModuleManager = module_manager
        
        self.format = self.config.config.config['format']

        self.choices:dict[str,list[tuple]] = changes_choices_by_format


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


    def get_preselected_answers(self) -> list[dict]:
        """check for possible preselected answers according the current format, make quuestions if is needed"""
        preselected_answers:list[dict] = []
        
        preselected_questions:list[PreselectedQuestion] = get_preselected_questions(format=self.format)
        
        for preselected_question in preselected_questions:
            question = preselected_question.get_value(self.module_manager) 
            if question :
                preselected_answers.append(question)
        
        return preselected_answers


    def get_answers(self):
        """Method to get the answers from the user
        1 - check for preselections
        2 - request filtered answers
        3 - set up all answers
        """
        # ------- automatic answers detection ----------

        # if we had preselected result then we can get them here
        preselected_answers:list[dict] = self.get_preselected_answers()
        # ------ automatic answers segregation and formating ---------
        request_optionals:bool = True if self.config.get_config("avoid_optionals") else False 
        
        preselected_answers_key_list:list[str] = [ list(key.keys())[0] for key in preselected_answers ]

        # ------ regular question prompting ------------

        normal_questions = get_questions(self.format, preselected_answers_key_list, request_optionals)

        normal_answers = inquirer.prompt(normal_questions[self.format])
        
        # print(normal_answers, preselected_answers)

        answers:dict = dict()
        for preselected_answer in preselected_answers:
            answers.update(preselected_answer)
        answers.update(normal_answers)
        
        # print(answers)

        if answers:
            # TODO: handle optional
            # if self.format in self.optional_questions and not request_optionals:
                # for question in self.optional_questions[self.format]:
                    # set_question = input(f"set the {question.name} (y,*): ")
                    # if set_question.lower() == 'y':
                        # temp_dict = inquirer.prompt({question})
                        # answers.update(temp_dict)
            # after optional question handling make a update
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
    
    
    #TODO: this souldnt live here -> use the repository
    def update_preselected_data(self):
        """Update modules file
        1 - get used module
        2 - get modules in file (in this point this module should exist in module manager)
        3 - search for our module inside the result
            3.1 -  if exist update counter and last used
            3.2 - if not exists addit to the list
                a - limit number of modules to write to 10
        4 - save the modules infomation
        """
        current_modules:list = self.module_manager.get_modules()
        new_modules:list[ModuleConfig] = []
        current_date = pendulum.now()
        exist_in_module_list:bool = False

        modules_as_csv = ""
        
        if current_modules and len(current_modules) > 0:
            for module in current_modules:
                if module.name.lower() == self.module.lower():
                    module.last_used = current_date.int_timestamp
                    module.use_count += 1
                    exist_in_module_list = True
                new_modules.append(module)
        
        if exist_in_module_list is False:
            new_module = ModuleConfig(self.module, current_date.int_timestamp, current_date.int_timestamp, 1)
            new_modules.append(new_module)

        new_modules.sort(key=lambda module: module.last_used, reverse=True)

        new_modules = new_modules[0:9:1]

        for module in new_modules:
            modules_as_csv += f"{module.name},{module.date},{module.last_used},{module.use_count}\n"

        
        # overwrite file
        file = open(".ignore.commitcli_modules", "w")

        file.write(modules_as_csv)
        file.close()




