from .GenericTask import GenericTask
import requests
from requests.exceptions import HTTPError


class HttpPingTask(GenericTask):

    def __init__(self, task=None):
        super(HttpPingTask, self).__init__(task=task)
        if task.get('url') is None:
            raise Exception('url must be set for http_ping')

        if self.task.get('ok_resp') is not None and isinstance(self.task['ok_resp'], list):
            self.ok_resp = self.task['ok_resp']
        else:
            self.ok_resp = [200, 301]

    def run(self):
        super(HttpPingTask, self).run()
        resp_code = None
        try:
            response = requests.get(url=self.task['url'], allow_redirects=False, timeout=self.task.get('timeout'))
            resp_code = response.status_code
            self.timings = (0, 0, int(response.elapsed.total_seconds() * 1000))
            response.raise_for_status()
        except HTTPError as http_err:
            return False, resp_code, str(http_err), self.timings
        except Exception as err:
            return False, resp_code, str(err), self.timings
        else:
            return self.ok_resp.count(resp_code) > 0, resp_code, 'Open {}: {} in {} = {}; total {}s'.format(
                self.task['url'], resp_code, str(self.ok_resp),
                str(self.ok_resp.count(resp_code) > 0), self.timings[2]/1000
            ), self.timings
