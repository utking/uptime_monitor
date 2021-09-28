from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


class EmailSender(object):

    def __init__(self):
        self.sender = settings.EMAIL_FROM

    def send_email(self, to: str, data: dict):
        receivers = [to]

        try:
            send_mail(
                subject='[Uptime Monitor] {} has Failed'.format(data['check_name']),
                message=render_to_string('mail_template.html', {
                    'name': data['check_name'],
                    'trace': data['trace'],
                    'status': data['status'],
                    'resp_code': data['resp_code'],
                    'datetime': data['created_at'],
                }),
                from_email=self.sender,
                recipient_list=receivers,
                fail_silently=False,
            )
        except Exception as ex:
            print("Error: unable to send email:", ex)
