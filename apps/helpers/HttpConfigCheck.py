from .GenericConfigCheck import GenericConfigCheck


class HttpConfigCheck(GenericConfigCheck):

    def __init__(self, check=None):
        super(HttpConfigCheck, self).__init__(check=check)

    def run(self):
        print(self.check)
        return True
