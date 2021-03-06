from .HttpPingTask import HttpPingTask
from .SelemiumTask import SeleniumTask
from .TestTask import TestTask
from apps.checks.models import CheckHistory
from apps.helpers.GenericTask import GenericTask


class GenericConfigCheck:
    class AndFlow(object):
        @staticmethod
        def run(check=None, tasks: list = None):
            errors = []
            ok = True
            code = None
            timings = (0, 0, 0)
            for task in tasks:
                task_cls = GenericConfigCheck.get_task(task['type'])
                if not issubclass(task_cls, GenericTask):
                    raise Exception('Unknown check task type in ', task)

                ok, code, context, task_timings = task_cls(task=task).run()
                timings = [a + b for a, b in zip(timings, task_timings)]
                if not ok:
                    errors.append(context)
                    CheckHistory(
                        check_id=check.id, name=check.name, timings=timings,
                        location=check.location, success=ok, resp_code=code,
                        result='\n'.join(errors)
                    ).save()
                    raise Exception('Task failed with code {};'.format(code), context)
                else:
                    errors.append(context)
            CheckHistory(
                check_id=check.id, name=check.name, timings=timings,
                location=check.location, success=ok, resp_code=code,
                result='\n'.join(errors)
            ).save()
            return True

    class OrFlow(object):
        @staticmethod
        def run(check=None, tasks: list = None):
            errors = []
            ok = False
            code = None
            timings = (0, 0, 0)
            for task in tasks:
                task_cls = GenericConfigCheck.get_task(task['type'])
                if not issubclass(task_cls, GenericTask):
                    raise Exception('Unknown check task type in ', task)

                ok, code, context, task_timings = task_cls(task=task).run()
                timings = [a + b for a, b in zip(timings, task_timings)]
                if ok:
                    errors.append(context)
                    CheckHistory(
                        check_id=check.id, name=check.name, timings=timings,
                        location=check.location, success=ok, resp_code=code,
                        result='\n'.join(errors)
                    ).save()
                    return True
                else:
                    errors.append(context)
            CheckHistory(
                check_id=check.id, name=check.name, timings=timings,
                location=check.location, success=ok, resp_code=code,
                result='\n'.join(errors)
            ).save()
            raise Exception('\n'.join(errors))

    TASK_MAP = {
        'test': TestTask,
        'http_ping': HttpPingTask,
        'xpath': SeleniumTask,
    }

    def __init__(self, check=None):
        # Initialize class fields
        self.check = None
        self.tasks = None
        self.flow_type = None
        # Initialize the fields from the check
        self.parse_config(check=check)

    def parse_config(self, check=None):
        if check is None or check.flow is None:
            raise Exception('Wrong check config')
        self.check = check
        self.flow_type = check.flow.get('type')
        self.tasks = check.flow.get('elements')
        if self.flow_type is None or self.flow_type not in ['or', 'and']:
            raise Exception('Wrong check flow')

    def run(self) -> bool:
        if self.flow_type == 'and':
            return self.AndFlow.run(check=self.check, tasks=self.tasks)
        elif self.flow_type == 'or':
            return self.OrFlow.run(check=self.check, tasks=self.tasks)
        return True

    @staticmethod
    def get_task(task_type: str):
        if isinstance(task_type, str):
            if GenericConfigCheck.TASK_MAP.get(task_type) is not None:
                return GenericConfigCheck.TASK_MAP[task_type]
        raise Exception('Unknown task type element', task_type)
