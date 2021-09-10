import sys
from django.core.management.base import BaseCommand
from apps.checks.views import run_checks


class Command(BaseCommand):
    help = 'Run checks'

    def __init__(self):
        super().__init__()
        self.file = None

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, nargs=1, help='A check definition file')

    def handle(self, *args, **options):
        if options['file']:
            self.file = options['file']
            print('All checks will be triggered')
        try:
            run_checks(check_id=None)
            self.stdout.write(self.style.SUCCESS('No errors'))
        except Exception as e:
            self.stderr.write(self.style.ERROR('Error'))
            print(e)
            sys.exit(1)
