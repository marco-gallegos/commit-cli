"""
@Author Marco A. Gallegos
@Date   2020/12/31
@Update 2020/12/31
@Description
    
"""

class Configuration(object):
    """

    Args:
        object ([type]): [description]
    """
    def __init__(self, config:dict=None, signgpg:bool=False):
        self.config = {
            'format': "odoo",
            'signgpg': signgpg,
        }

        if config:
            self.config['format'] = config['format'] if 'format' in config else self.config['format']
            self.config['signgpg'] = config['signgpg'] if 'format' in config[] else self.config['signgpg']

        self.supported_formats = [
            "odoo",
            "sgc",
            "cc",
            "free",
        ]

        def __str__(self):
            return f"configuracion|  format: {self.config['format']} || sign: {self.config['signgpg']}"