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
from common.logger import logger

class CommitMessage(object):
    """This clas is a abstraction of a commit message,
    this class must to generate a formatted commit string

    Args:
        object (object): base object from python
    """
    
    def __init__(
        self,
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
        self.moduleid = None # module id only set when answer comes from preselected answers
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
            # platform specific fixes
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
            
            if 'moduleid' in answers.keys() and answers['moduleid'] :
                logger.log("INFO", f"seting module id {answers['moduleid']}")
                self.moduleid = answers['moduleid']
            return True
        else:
            return False


    def get_preselected_answers(self) -> list[dict]:
        """check for possible preselected answers according the current format, make quuestions if is needed"""
        preselected_answers:list[dict] = []
        
        preselected_questions:list[PreselectedQuestion] = get_preselected_questions(format=self.format)
        
        for preselected_question in preselected_questions:
            # this calls a functions asigned to get_value
            answer:dict = preselected_question.get_value(self.module_manager) 
            if len(answer.keys()) > 0 :
                for key in answer.keys():
                    preselected_answers.append({ key: answer[key] })
        
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

        logger.log("INFO", preselected_answers)

        logger.log("INFO", "=====================")

        # -------------- speciaol changes --------------
        # ------ regular question prompting ------------

        normal_questions = get_questions(self.format, preselected_answers_key_list, request_optionals)

        normal_answers = inquirer.prompt(normal_questions[self.format])
        

        answers:dict = dict()
        for preselected_answer in preselected_answers:
            answers.update(preselected_answer)
        
        logger.log("INFO", normal_answers)

        answers.update(normal_answers)

        logger.log("INFO", answers)
        
        if answers:
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
            logger.log("INFO", self.format)
            cc_format_minimum_requirements:bool = self.tag and len(self.tag) > 0 and len(self.header) > 0
            logger.log("INFO", cc_format_minimum_requirements)
            return cc_format_minimum_requirements
        else:
            return False
    
