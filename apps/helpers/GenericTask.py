

class GenericTask:

    def __init__(self, task=None):
        self.task = task
        self.type = task['type']
        self.timeout = task.get('timeout')
        self.timings = (0, 0, 0)

    def run(self):
        if self.task is None:
            raise Exception('Task cannot be None')
