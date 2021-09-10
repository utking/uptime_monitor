import sys
from django.core.management.base import BaseCommand
from apps.checks.views import reload_checks


class Command(BaseCommand):
    help = 'Verify/reload config files'

    def __init__(self):
        super().__init__()
        self.save = False

    def add_arguments(self, parser):
        parser.add_argument('--save', action='store_true', help='Save after verified')

    def handle(self, *args, **options):
        if options['save']:
            self.save = True
            print('Configuration will be saved after verified')
        try:
            checks = reload_checks(save=self.save)
            self.stdout.write(self.style.SUCCESS('No errors'))
        except Exception as e:
            self.stderr.write(self.style.ERROR('Verification error'))
            print(e)
            sys.exit(1)
