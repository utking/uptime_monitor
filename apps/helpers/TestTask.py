from .GenericTask import GenericTask


class TestTask(GenericTask):

    def __init__(self, task=None):
        super(TestTask, self).__init__(task=task)

    def run(self):
        super(TestTask, self).run()
        return True, None, '', self.timings
