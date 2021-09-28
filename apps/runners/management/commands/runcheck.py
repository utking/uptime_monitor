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

    def handle(self, *args, **options):
        if options['check_name']:
            self.check_name = options['check_name']
            print('A check for "{}" will be triggered'.format(self.check_name))
        else:
            print('All checks will be triggered')
        try:
            run_checks(check_id=self.check_name)
            self.stdout.write(self.style.SUCCESS('No errors'))
        except Exception as e:
            self.stderr.write(self.style.ERROR('Error'))
            print(e)
            sys.exit(1)
