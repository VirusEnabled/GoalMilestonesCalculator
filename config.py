class Config(object):
    def __init__(self):
        self.config = self.load_config()

    # need to fix this data gatherer
    def load_config(self):
        file = '.env'
        with open(file,'r') as file:
            lines = file.readlines()
            return {key.split('=')[0]: self.remove_black_space(key.split('=')[1]) for key in lines}

    def get_item(self, key):
        """
        gets the value from the configuration object
        :param key: str
        :return: str
        """
        return self.config[key] if key in self.config.keys() else None

    def remove_black_space(self,string):
        """
        serializes the string so that it doesn't have new line chars
        :param string: str
        :return: str
        """
        return string[:string.find('\n')]

    @property
    def get_site_env(self):
        """
        get the enviroment for the application,
        this helps you to actually manage properly
        when to use either production or development
        for the app.
        if env variable is set for production it will
        return True else False
        :return: bool
        """
        return self.config['SITE_ENVIRONMENT'] == 'DEV'