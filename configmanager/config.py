"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    Configuration is a class to contain and validate the configuration
"""
import os


class Configuration(object):
    config: dict = {
        "format": None,
        "signgpg": None,
        "avoid_optionals": False,
    }
    supported_formats: list = [
        "odoo",
        "sgc",
        "cc",
        "free",
    ]

    def __init__(self, config: dict = None, signgpg: bool = False, override_config: dict = None):
        self.config = {
            'format': "odoo",
            'signgpg': signgpg,
            'avoid_optionals': override_config['avoid_optionals'] if override_config else False
        }

        self.supported_formats = [
            "odoo",
            "sgc",
            "cc",
            "free",
        ]

        if config:
            self.config['format'] = config['format'].lower() if 'format' in config else self.config['format'].lower()
            self.config['signgpg'] = config['signgpg'] if 'signgpg' in config else self.config['signgpg']

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
               f" || avoid_optionals: {self.config['avoid_optionals']}"
    
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
            "signgpg={sign}"\
        
        if filled:
            return file_template.format(format=self.config['format'], sign=self.config['signgpg'])
        else:
            return file_template
