import sys
from django.core.management.base import BaseCommand
from apps.checks.views import run_checks


class Command(BaseCommand):
    help = 'Run checks'

    def __init__(self):
        super().__init__()
        self.check_name = None
        self.all_checks = True

    def add_arguments(self, parser):
        parser.add_argument('-c', '--check-name', type=str, help='A check name to run')
        parser.add_argument('-a', '--all-checks', action='store_true', help='Run all checks (default)')

    def handle(self, *args, **options):
        if options['check_name']:
            self.check_name = options['check_name']
            self.all_checks = False
            print('A check for "{}" will be triggered'.format(self.check_name))
            if options['all_checks']:
                raise Exception('Parameters -a and -c cannot be used together')
        else:
            print('All checks will be triggered')
        try:
            run_checks(check_id=self.check_name)
            self.stdout.write(self.style.SUCCESS('No errors'))
        except Exception as e:
            self.stderr.write(self.style.ERROR('Error'))
            print(e)
            sys.exit(1)
