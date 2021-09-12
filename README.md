# uptime_monitor

An Uptime Monitor with an extensible checking mechanism

## Prerequisites

* Python3.6+
* SQLite 3+ or MySQL 5.7+
* Selenium driver (check Selenium official documentation)

## How-To

### Install the application

* Clone the repository
* Run `pip3 install -r requirements.txt`
* Copy conf.d.example to conf.d and create the checks you need
* Copy monitor/settings.example.py to monitor/settings.py, read and adjust (SQL, SMTP, notifications, etc)
* Run `python3 managey.py migrate` to apply all required migrations
* Run `python3 managey.py createsuperuser` to add an admin panel user
* Run `python3 managey.py test` to run the available unit tests
* Create configuration files under conf.d (or any other folder you set in settings.py as the base path for config files)
* Run `python3 managey.py verify` to check the Yaml configuration files you created above
* Run `python3 managey.py verify --save` to add the configs to the SQL database you configured in settings.py
* Run `python3 managey.py runcheck` to run all the configured checks OR
* Run `python3 managey.py runcheck --file <check_id>` to run only the check with the ID

### Yaml configuration primer

```yaml
id: 'check_id'                              # Required - Uniq ID for the check config
name: 'Transactional Check'                 # Required - Human-readable name
flow:                                       # Required - tree-description of the check flow
  and:                                      # Required - type of the flow - can be either "or" or "and"
                                            # Flow items (http_ping|xpath)
                                            #   type http_ping
    - name: 'Check HTTP'                    # required - item name
      type: 'http_ping'                     # required - item type
      url: 'http://example.com'             # http_ping: required - URL to check
      ok_resp:                              # http_ping: optional - which codes count as a good response
        - 301
      timeout: 60                           # required - timeout after which an error will be thrown
                                            #   type xpath
    - name: 'Find #primary-menu'            # requires - item name
      type: 'xpath'                         # required - item type
      url: 'https://example.com'            # xpath: required - URL to check
      elements:                             # xpath: required - check tree-description for the check (AND-logic default)
        - or:                               # OR-logic for the first set of tasks in the check
          - find: '//*[@id="loginform-rememberme"]'       # find the XPath on the page
          - find: '//*[@id="colophon"]'                   # find the XPath on the page
          - find: '//*[@id="primary-menu"]'               # find the XPath on the page
        - set_value: '//*[@id="loginform-username"]'      # find the input on the page and set its value 
          value: 'user'                                   # the value to set
        - set_value: '//*[@id="loginform-password"]'      # find the input on the page and set its value
          value: 'password'                               # the value to set
        - click: '//*[@id="login-form"]/div[5]/button'    # find the button on the page and click on it
        - wait: 5                                         # sleep for 5 sec
        - get_text: '//*[@id="login-form"]/div[5]/button' # find the button on the page and check its text
          value: 'Log in'                                 # it must contain the value
      timeout: 60                                         # required - timeout after which an error will be thrown
verbose: false
location: 'azure'                                         # required - from which location we run the check
tags:                                                     # optional - tags for the check
  - 'prod'
  - 'azure'
notify:                                                   # optional - notification settings
  channel: 'opsgenie'                                     # notification channel
#  recipient: 'opsgenie'                                  # for the email channel - notification recipient(s)
```