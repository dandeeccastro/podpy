class ConfigError(Exception):
    pass

class ImproperFolderConfigurationException(ConfigError):   
    def __init__(self,message):
        self.message = message