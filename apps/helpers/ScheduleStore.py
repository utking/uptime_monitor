from apscheduler.schedulers.background import BackgroundScheduler


class ScheduleStore(object):
    __instance = None
    scheduler = None

    def __create_scheduler(self):
        print('Creating a scheduler store')
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def get_scheduler(self):
        return self.scheduler

    @staticmethod
    def get_instance():
        if ScheduleStore.__instance is None:
            ScheduleStore().__create_scheduler()
        return ScheduleStore.__instance

    def __init__(self):
        if ScheduleStore.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ScheduleStore.__instance = self
