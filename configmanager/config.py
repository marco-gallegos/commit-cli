"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    Configuration is a class to contain and validate the configuration
"""
import os

class Configuration(object):
    def __init__(self, config:dict=None, signgpg:bool=False):
        self.config = {
            'format': "odoo",
            'signgpg': signgpg,
        }

        self.supported_formats = [
            "odoo",
            "sgc",
            "cc",
            "free",
        ]

        if config:
            self.config['format'] = config['format'].lower() if 'format' in config else self.config['format']
            self.config['signgpg'] = config['signgpg'] if 'signgpg' in config else self.config['signgpg']
            self.config['format'] = self.config['format'].lower()

            if self.config['signgpg'] and not self.can_sign_gpg():
                print("Tu configuracion solicita firmar commits pero git no esta configurado")
                self.config['signgpg']=False
            if not (self.config['format'] in self.supported_formats):
                print(f"el formato {self.config['format']} no es soportado, por defecto usaremos el formato de {self.supported_formats[0]}")
                self.config['format']=self.supported_formats[0]

        self.can_sign_gpg()

    
    def __str__(self)->str:
        return f"configuracion|  format: {self.config['format']} || sign: {self.config['signgpg']}"

    
    def can_sign_gpg(self)->bool:
        signkey = os.popen("git config --global user.signingkey").read() 
        if not signkey :
            return False
        else:
            return True


    def is_a_valid_format(self, format:str)->bool:
        return format in self.supported_formats


    def get_configuration_file_string(self, filled:bool=True)->str:
        file_template = "#Format for every commit\n"\
        "#supported formats free, odoo, sgc(semantic git commits) and cc (conventional commits)\n"\
        "format={format}\n\n"\
        "#Option to sign the commits o every commit, must be True or False\n"\
        "signgpg={sign}"\
        
        if filled:
            return file_template.format(format=self.config['format'], sign=self.config['signgpg'])
        else:
            return file_template
