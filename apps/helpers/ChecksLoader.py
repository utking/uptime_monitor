from .config_loader import load_file
from .GenericLoader import GenericLoader


class ChecksLoader(GenericLoader):

    services = []
    required_fields = [
        'id',
        'name',
        'location',
    ]

    def __init__(self, base_path=None, checks=None):
        super(ChecksLoader, self).__init__(base_path=base_path, checks=checks)

    def load(self):
        self.checks = []
        self.config_files.clear()
        check_names = []

        self.get_config_files()
        for full_path in self.config_files:
            check = load_file(full_path)
            if check is None:
                raise Exception('Check definition Error in {}'.format(full_path))

            self.check_required(check)
            self.check_already_exists(check['name'], check_names)
            if self.__validate(check):
                check_names.append(check['name'])
                self.checks.append(check)

        print('Loading checks from {} Completed: {} checks total'.format(self.BASE_PATH, len(self.checks)))
        return self.checks

    @staticmethod
    def __validate(check=None):
        if check.get('flow') is None or not isinstance(check['flow'], dict):
            raise Exception('"flow" is missing in the check definition')
        flow = check['flow']
        if flow.get('and') is None and flow.get('or') is None:
            raise Exception('Flow "{}" does not have AND or OR branches'.format(check['name']))
        if flow.get('and') is not None and flow.get('or') is not None:
            raise Exception('Flow "{}" has both AND or OR branches, while only one can exist'.format(check['name']))
        return True
