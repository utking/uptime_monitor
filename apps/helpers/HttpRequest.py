import requests
from requests import Response
import datetime


class HttpResponse(Response):
    def __init__(self):
        super(HttpResponse, self).__init__()
        self.status_code = 200
        self.raw = 'response'
        self.elapsed = datetime.timedelta(0)


class HttpMockBackend(object):
    @staticmethod
    def get(url, params=None, **kwargs):
        return HttpResponse()


class HttpRequest(object):
    def __init__(self, backend=None):
        if backend is None:
            self.requests = requests
        else:
            self.requests = backend

    def get(self, url, params=None, **kwargs):
        return self.requests.get(url=url, params=params, **kwargs)
