from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = 'apps.schedule'
    run_already = False

    def ready(self):
        if not self.run_already:
            self.run_already = True
            from apps.schedule.views import populate_schedule
            populate_schedule()
