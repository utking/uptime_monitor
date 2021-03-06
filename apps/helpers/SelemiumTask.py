from .GenericTask import GenericTask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class XPathFind(object):

    @staticmethod
    def get_browser(url=None, timeout=None):
        if timeout is None:
            timeout = 60
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options)
        backend_perf, frontend_perf, total_perf = 0, 0, 0
        if isinstance(url, str):
            driver.set_page_load_timeout(time_to_wait=timeout)
            driver.get(url)
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            response_start = driver.execute_script("return window.performance.timing.responseStart")
            dom_complete = driver.execute_script("return window.performance.timing.domComplete")

            backend_perf = response_start - navigation_start
            frontend_perf = dom_complete - response_start
            total_perf = dom_complete - navigation_start

        return driver, (backend_perf, frontend_perf, total_perf)

    @staticmethod
    def get_el(driver, el) -> (any, str):
        if isinstance(el, str):
            try:
                elem = driver.find_element_by_xpath(el)
                if elem is None:
                    return None, '{} was not found on the page'.format(el)
                else:
                    return elem, '{} was found on the page'.format(el)
            except Exception as ex:
                return None, ex
        return None, 'Wrong XPath'


class XPathGenericTask(object):
    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True):
        raise Exception("run() must be implemented")


class XPathFindTask(XPathGenericTask):

    def __init__(self):
        super(self.__class__, self).__init__()

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        try:
            elem, context = XPathFind.get_el(driver=driver, el=el['selector'])
            if elem is None:
                return False, context
            else:
                return True, context
        except Exception as ex:
            return False, str(ex)


class XPathClickTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        elem, context = XPathFind.get_el(driver=driver, el=el['selector'])
        if elem is None:
            return False, context
        else:
            elem.click()
            return True, '{}\n{} was clicked'.format(context, el['selector'])


class XPathGetTextTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        if el.get('value') is None or not isinstance(el['value'], str):
            raise Exception('Value for comparison must be a string', type(el['value']), 'given')
        elem, context = XPathFind.get_el(driver=driver, el=el['selector'])
        if elem is None:
            return False, context
        text = elem.text
        if text.find(el['value']) != -1:
            return True, '{}\n{}; text includes "{}"'.format(context, el['selector'], el['value'])
        else:
            return False, '{}\n"{}" was not found in "{}"'.format(context, el['value'], text)


class XPathGetValueTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        if el.get('value') is None or not isinstance(el['value'], str):
            raise Exception('Value for comparison must be a string', type(el['value']), 'given')
        elem, context = XPathFind.get_el(driver=driver, el=el['selector'])
        if elem is None:
            return False, context
        value = elem.get_attribute('value')
        if value == el['value']:
            return True, '{}\n{}; value is "{}"'.format(context, el['selector'], el['value'])
        else:
            return False, '{}\n"{}"\'s value "{}" is not {}'.format(context, el['selector'], value, el['value'])


class XPathSetValueTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        if el.get('value') is None or not isinstance(el['value'], str):
            raise Exception('Value for comparison must be a string', type(el['value']), 'given')
        elem, context = XPathFind.get_el(driver=driver, el=el['selector'])
        if elem is None:
            return False, context
        elem.send_keys(el['value'])
        return True, '{}\nValue for "{}" was set to "{}"'.format(context, el['selector'], el['value'])


class XPathAndTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True) -> (bool, str):
        if el.get('type') is None or el.get('type') != 'and':
            raise Exception('Wrong element for XPathAndTask')
        context = None
        for el in el['elements']:
            task = TaskMapper.get_task(el['type'])
            if not issubclass(task, XPathGenericTask):
                raise Exception('Wrong XPath task in ', el)
            ok, context = task.run(driver=driver, el=el)
            if not ok:
                return ok, context
        return True, context


class XPathOrTask(XPathGenericTask):

    def __init__(self, xpath=None):
        super(self.__class__, self).__init__(xpath=xpath)

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=False) -> (bool, str):
        if el.get('type') is None or el.get('type') != 'or':
            raise Exception('Wrong element for XPathOrTask')
        errors = []
        for el in el['elements']:
            task = TaskMapper.get_task(el)
            if not issubclass(task, XPathGenericTask):
                raise Exception('Wrong XPath task in ', el)
            ok, context = task.run(driver=driver, el=el)
            if ok:
                errors.append(context)
                return True, '\n'.join([str(i) for i in errors if i])
            else:
                errors.append(context)
        return False, '\n'.join(errors)


class XPathWaitTask(XPathGenericTask):

    def __init__(self):
        super(self.__class__, self).__init__()

    @staticmethod
    def run(driver=None, el=None, exit_on_fail=True):
        try:
            interval = int(el['value'])
            if interval <= 0:
                raise Exception()
        except:
            return False, 'Wait interval must be an integer and greater than 0'
        driver.implicitly_wait(time_to_wait=interval)
        return True, 'Slept for {} sec'.format(interval)


class SeleniumTask(GenericTask):

    def __init__(self, task=None):
        super(self.__class__, self).__init__(task=task)
        self.context = []
        self.timings = (0, 0, 0)

    def get_context(self):
        return 'Selenium GET Timings backend={}s, frontend={}s, total={}s\n{}'.format(
            self.timings[0]/1000, self.timings[1]/1000, self.timings[2]/1000,
            '\n'.join([str(i) for i in self.context if i]))

    def run(self) -> (bool, int, str):
        super(self.__class__, self).run()
        driver = None

        try:
            driver, self.timings = XPathFind.get_browser(self.task['url'], timeout=self.task.get('timeout'))

            for el in self.task['elements']:
                task = TaskMapper.get_task(el)
                if not issubclass(task, XPathGenericTask):
                    raise Exception('Wrong XPath task in ', el)
                ok, context = task.run(driver=driver, el=el)
                if not ok:
                    raise Exception(context)
                else:
                    self.context.append(context)
            driver.close()
        except Exception as err:
            self.context.append(str(err))
            if driver is not None:
                driver.close()
            return False, None, self.get_context(), self.timings
        else:
            return True, None, self.get_context(), self.timings


class TaskMapper(object):
    TASK_MAP = {
        'get_text': XPathGetTextTask,
        'get_value': XPathGetValueTask,
        'set_value': XPathSetValueTask,
        'find': XPathFindTask,
        'click': XPathClickTask,
        'wait': XPathWaitTask,
        'and': XPathAndTask,
        'or': XPathOrTask,
    }

    @staticmethod
    def get_task(el):
        if isinstance(el, dict) and el.get('type') is not None:
            task_type = el.get('type')
            if task_type in TaskMapper.TASK_MAP.keys():
                return TaskMapper.TASK_MAP[task_type]
        else:
            raise Exception('Unknown XPath element', el)
        return None
