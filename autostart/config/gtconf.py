
from dotted.collection import DottedDict
import yaml
from pyaml_env import parse_config
import dotenv

class _Config:

    def __init__(self):
        self.relativ_config_path = 'config/config.yml'
        self.config = DottedDict(self._load_config_env_file(self.relativ_config_path))


    @staticmethod
    def _load_config_file(path):
        """ Load Config File normal"""

        with open(path) as file:
            config_content = yaml.load(file, Loader=yaml.FullLoader)
        
        return config_content

    @staticmethod
    def _load_config_env_file(path):
        """ Load YAML Config File with enviroment variables"""

        # run load_dotenv file to load env file vars

        dotenv.load_dotenv()

        config_content = parse_config(path)
        return config_content

configeration = _Config() #! used as _Singleton - only creat one and only one _config instance.
CONFIG = configeration.config
