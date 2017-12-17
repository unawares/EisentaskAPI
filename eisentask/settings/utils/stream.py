import json
from django.core.exceptions import ImproperlyConfigured

class SettingsFile:
    def __init__(self, path):
        with open(path) as f:
            self.configs = json.loads(f.read())

    def get_env_var(self, setting):
        try:
            val = self.configs[setting]
            if val == 'True':
                val = True
            elif val == 'False':
                val = False
            return val
        except KeyError:
            error_msg = 'ImproperlyConfigured: ' \
                                'Set {0} environment variable'.format(setting)
            raise ImproperlyConfigured(error_msg)
