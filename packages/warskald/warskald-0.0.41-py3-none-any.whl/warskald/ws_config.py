import configparser
import json
import os
import toml
import yaml

from configparser import MissingSectionHeaderError
from typing import Any
from warskald import utils, AttrDict

ENV_PROPS_DIR = os.environ.get('ENV_PROP_DIR', os.path.expanduser('~/.config/env_props'))

class SimpleConfigParser(configparser.ConfigParser):
    """ SimpleConfigParser class to handle configuration files without sections """
    
    def read(self, filenames, encoding=None):
        """ Method to read the configuration file and add a dummy section if one is not present

        Note: Override of configparser.ConfigParser.read
        
        Args:
            filenames (_type_): Names of the configuration files to read
            encoding (str, optional): String encoding to use. Defaults to None.
        """
                    
        if isinstance(filenames, str):
            filenames = [filenames]
        for filename in filenames:
            with open(filename, 'r', encoding=encoding) as config_file:
                content = config_file.read()
                if(not content.startswith('[dummy_section]')):
                    content = '[dummy_section]\n' + content
                
                self.read_string(content)
                
class ConfigReader:
    """ Class to read configuration files and return the data as an AttrDict """
    
    def __init__(self, config_path: str) -> None:
        """ Constructor for the ConfigReader class

        Args:
            config_path (str): The path to the configuration file
        Raises:
            FileNotFoundError: Raised if the configuration file is not found
        """
                
        self.config_data: AttrDict = AttrDict()
        self.path = config_path
        
        if(not os.path.exists(config_path)):
            raise FileNotFoundError(f'Config file not found: {config_path}')
        
        self._parse_config(config_path)
    
    def _parse_config(self):
        """ Method to parse the configuration file and store the data in an AttrDict """

        # Get the values and extension of the file
        config_data, cfg_type = self._read_config(self.config_path)
        
        # Initialize the config_data attribute
        self.config_data = AttrDict({})
        
        # Handle configparser and dict types
        if(isinstance(config_data, configparser.ConfigParser)):
            for section in config_data.sections():
                if(section != 'dummy_section'):
                    # Initialize the section in the config_data attribute
                    # ignoring the dummy_section added by SimpleConfigParser
                    self.config_data[section] = {}
                    
                for key, value in config_data.items(section):
                    # Add the appropriate values from the section to the config_data attribute
                    if(utils.not_empty(value)):
                        if(section == 'dummy_section'):
                            self.config_data[key] = value
                        else:
                            self.config_data[section][key] = value
                   
        elif(cfg_type == 'dict'):
            # Add the values from the dictionary to the config_data attribute
            self.config_data = AttrDict(config_data)
    
    def _read_config(self):
        """ Method to read the configuration file and return the data as a dictionary

        Raises:
            ValueError: Raised if the configuration file extension is not supported

        Returns:
            dict | configparser.ConfigParser: The configuration data as a dictionary or ConfigParser object
        """

        # Get the extension of the file
        _, ext = os.path.splitext(self.path)
        
        # Read the file based on the extension
        if ext == '.json':
            with open(self.path, 'r') as file:
                return json.load(file), 'dict'
            
        elif ext == '.ini':
            try:
                config = configparser.ConfigParser()
                config.read(self.path)
                return config, 'configparser'
            except MissingSectionHeaderError:
                config = SimpleConfigParser()
                config.read(self.path)
                return config, 'SimpleConfigParser'
            
        elif ext in ['.properties', '.conf']:
            config = SimpleConfigParser()
            config.read(self.path)
            
            return config, 'SimpleConfigParser'
        
        elif ext == '.yaml' or ext == '.yml':
            with open(self.path, 'r') as file:
                return yaml.safe_load(file), 'dict'
            
        elif ext == '.toml':
            with open(self.path, 'r') as file:
                return toml.load(file), 'dict'
            
        else:
            raise ValueError(f'Unsupported config file extension: {ext}')
                
class EnvironmentProps:
    """ Class that combines all the environment properties into a single dictionary for easy retrieval 
    
        The path to the environment properties directory is retrieved from the 
        ENV_PROP_DIR environment variable (unless a path is provided as an 
        argument) and the properties from all .json, .cfg, .ini, .properties, 
        .toml, and .yaml files in the directory are combined into a single 
        dictionary, unless a specific list of files is provided.
    """
    
    def __init__(self, env_props_dir: str = None, specific_files: list[str] = None):
        """ Constructor for the EnvironmentProps class
            
        Args:
            env_props_dir (str, optional): The path to the environment properties directory. Defaults to None.
            specific_files (list[str], optional): A list of specific files to parse. Defaults to [].
        Raises:
            FileNotFoundError: Raised if the environment properties directory or
                a specific file is not found
            NotADirectoryError: Raised if the path provided is not a directory
        """
        
        env_props_dir = env_props_dir if env_props_dir else ENV_PROPS_DIR
        
        if(not os.path.exists(env_props_dir)):
            raise FileNotFoundError(f'Environment properties directory not found: {env_props_dir}\nPlease set the ENV_PROP_DIR environment variable to the correct path.')
        if(not os.path.isdir(env_props_dir)):
            raise NotADirectoryError(f'Path is not a directory: {env_props_dir}\nPlease set the ENV_PROP_DIR environment variable to the correct path that is a directory.')
        
        env_prop_files = specific_files if specific_files else os.listdir(env_props_dir)
        
        for prop_file in env_prop_files:
            if(not os.path.exists(os.path.join(env_props_dir, prop_file))):
                raise FileNotFoundError(f'Environment property file not found: {prop_file}')
        
        self.config = AttrDict({})
        
        self._parse_configs([os.path.join(env_props_dir, file) for file in env_prop_files])
    
    def _parse_configs(self, file_paths: list[str]) -> None:
        """ Method to parse the environment properties files and combine them into a single dictionary

        Args:
            file_paths (list[str]): A list of file paths to the environment properties files
        """
                
        for file_path in file_paths:
            config = ConfigReader(file_path).config_data
            
            if(isinstance(config, dict)):
                for key, value in config.items():
                    self.config[key] = value
            
    def get(self, path: str | list[str], default_val: Any = None) -> Any:
        """ Method to retrieve a value from the environment properties dictionary

        Args:
            path (str | list[str]): The path to the value in the dictionary
            default_val (Any, optional): The default value to return if the path is not found. Defaults to None.

        Returns:
            Any: The value at the specified path in the dictionary, or the default value if the path is not found
        """
        
        value = utils.get_nested(self.config, path, default_val)
        if(isinstance(value, dict)):
            return AttrDict(value)
        return value
    
    def set(self, cfg_file: str, key: str | list[str], value: Any):
        """ Method to set a value in a configuration file

        Args:
            cfg_file (str): Config file name (with extension) in the environment properties directory
            key (str | list[str]): The key path to the value to set
            value (Any): The value to set

        Raises:
            FileNotFoundError: Raised if the config file is not found
        """
        
        # Check if the config file exists        
        path = os.path.join(ENV_PROPS_DIR, cfg_file)
        if(not os.path.exists(path)):
            raise FileNotFoundError(f'Config file not found: {path}')
        
        # Normalize the key path
        if(isinstance(key, str)):
            key = key.split('.')
        
        if(isinstance(key, list)):
            
            # Get the extension of the file
            ext = os.path.splitext(path)[1]
            
            # Read the file and set the value based on the extension
            if(ext == '.json'):
                with open(path, 'r') as file:
                    data = json.load(file)
                
                utils.set_nested(data, key, value)
                
                with open(path, 'w') as file:
                    json.dump(data, file)
                    
            elif(ext == 'toml'):
                with open(path, 'r') as file:
                    data = toml.load(file)
                
                utils.set_nested(data, key, value)
                
                with open(path, 'w') as file:
                    toml.dump(data, file)
                    
            elif(ext == '.yaml' or ext == '.yml'):
                with open(path, 'r') as file:
                    data = yaml.safe_load(file)
                
                utils.set_nested(data, key, value)
                
                with open(path, 'w') as file:
                    yaml.dump(data, file)
                    
            elif(ext == '.ini' or ext == '.properties' or ext == '.conf'):
                config = SimpleConfigParser()
                config.read(path)
                
                if(len(key) == 1):
                    config[key[0]] = value
                else:
                    config[key[0]][key[1]] = value
                
                with open(path, 'w') as file:
                    config.write(file)