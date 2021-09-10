from . import config_loader


class GenericLoader(object):
    BASE_PATH = None
    required_fields = None
    config_files = set()
    checks = []

    def __init__(self, base_path=None, checks=None):
        self.BASE_PATH = base_path
        if checks is not None:
            self.checks = checks

        if not isinstance(self.required_fields, list):
            raise Exception('Required fields list must be provided', type(self).__name__)

    def get_config_files(self):
        self.config_files = config_loader.ConfigLoader(self.BASE_PATH).get_config_files()

    def check_required(self, config=None):
        for field in self.required_fields:
            if config.get(field) is None:
                if field == 'name':
                    name = config
                else:
                    name = config['name']
                raise Exception('{} {} has no required field "{}"'.format(
                    type(self).__name__,
                    name,
                    field))
        return False

    def check_already_exists(self, item, items):
        if item in items:
            raise Exception('{} {} is already in the config'.format(type(self).__name__, item))
