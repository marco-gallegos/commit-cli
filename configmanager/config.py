"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    Configuration is a class to contain and validate the configuration
"""
import os
from common.functions import get_project_id

class TypeConfigurationConfig(object):
    format:str
    signgpg:bool
    avoid_optionals: bool
    db:str
    db_url:str
    db_port:str
    db_name:str
    db_user:str
    db_password:str
    projectid:str
    
    def __init__(self, format='cc', signgpg=False, avoid_optionals=False,
                 db='localfile', db_url='localhost', db_port='27017', db_name='commitcli',
                 db_user='', db_password=''):
        self.format = format
        self.signgpg = signgpg
        self.avoid_optionals = avoid_optionals
        self.db = db
        self.db_url = db_url
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.projectid = get_project_id()

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        else:
            raise KeyError(f"'TypeConfigurationConfig' object has no attribute '{clave}'")

    def __setitem__(self, clave, valor):
        if hasattr(self, clave):
            setattr(self, clave, valor)
        else:
            raise KeyError(f"'TypeConfigurationConfig' object has no attribute '{clave}'")

class Configuration(object):
    config:TypeConfigurationConfig
    supported_formats: list = [
        "odoo",
        "sgc",
        "cc",
        "free",
    ]

    supported_db: list = [
        "localfile",
        "mongodb",
    ]

    def __init__(self, config:dict = None, signgpg: bool = False, override_config: dict = None) -> None:
        avoid_optionals = override_config['avoid_optionals'] if override_config else False
        self.config:TypeConfigurationConfig = TypeConfigurationConfig(signgpg= signgpg, avoid_optionals= avoid_optionals)

        if config:
            self.config['format'] = config['format'].lower() if 'format' in config else self.config['format']
            self.config['signgpg'] = config['signgpg'] if 'signgpg' in config else self.config['signgpg']
            
            self.config['db'] = config['db'].lower() if 'db' in config else self.config['db']
            self.config['db_url'] = config['db_url'].lower() if 'db_url' in config else self.config['db_url']
            self.config['db_port'] = config['db_port'] if 'db_port' in config else self.config["db_port"]
            self.config['db_name'] = config['db_name'] if 'db_name' in config else self.config["db_name"]
            self.config['db_user'] = config['db_user'] if 'db_user' in config else self.config['db_user']
            self.config['db_password'] = config['db_password'] if 'db_password' in config else self.config['db_password']

            if self.config['signgpg'] and not self.can_sign_gpg():
                print("Tu configuracion solicita firmar commits pero git no esta configurado")
                self.config['signgpg']=False
            if not (self.config['format'] in self.supported_formats):
                print(
                    f"{self.config['format']} is not a supported format, instead we will use "
                    f"{self.supported_formats[0]} as default"
                )
                self.config['format'] = self.supported_formats[0]


        self.can_sign_gpg()


    def __str__(self)->str:
        """Return a string representation of the object, this function
        is called by the built in print function

        :return: string representation
        :rtype: str
        """
        return f"configuracion->  format: {self.config['format']} || sign: {self.config['signgpg']}" \
                f" || avoid_optionals: {self.config['avoid_optionals']} \ndb : {self.config['db']}" \
                f"\ndb url: {self.config['db_url']}" \
                f"\ndb port: {self.config['db_port']}"


    def can_sign_gpg(self)->bool:
        """Return true if the users git repository is configured to sign the commits

        :return: indicates that the user can sign the commits
        :rtype: bool
        """
        signkey = os.popen("git config --global user.signingkey").read() 
        if not signkey :
            return False
        else:
            return True


    def is_a_valid_format(self, format: str) -> bool:
        """Return true if the format parameter string is a supported commit format.

        :param format: format to evaluate
        :type format: str
        :return: boolean if the format is supported
        :rtype: bool
        """
        return format in self.supported_formats


    def get_configuration_file_string(self, filled: bool = True) -> str:
        """This method returns the string to store the configuration file,
        optionally this function return the string template.

        :param filled: if you want the filled string or the template string, defaults to True
        :type filled: bool, optional
        :return: format string
        :rtype: str
        """
        file_template = "#Format for every commit\n"\
            "#supported formats free, odoo, sgc(semantic git commits) and cc (conventional commits)\n"\
            "format={format}\n\n"\
            "#Option to sign the commits o every commit, must be True or False\n"\
            "signgpg={sign}\n"\
            "\n"\
            "#db configuration\n"\
            "db=localfile\n"\
            "db_url=localhost\n"\
            "db_port=27017\n"\
            "db_name=commitcli\n"\
            "db_user=\n"\
            "db_password="\
        
        if filled:
            return file_template.format(format=self.config['format'], sign=self.config['signgpg'])
        else:
            return file_template
