from .media import send_email, send_sms
from celery import shared_task
# from time import sleep
from .celery import app as celery_app
from django.conf import settings
import logging

logger = logging.getLogger("project.task")

def celery_up():
    return bool(celery_app.control.inspect(timeout=settings.CELERY_INSPECT_TIMEOUT).active())


# @celery_app.task
@shared_task()
def send_email_async(*args, **kwargs):
    logger.info('start send email')
    if settings.ENVIRONMENT_APP == 'DEVELOPE':
        logger.info('bypass send email in develop env')

        subject = kwargs.get('subject', '')
        to = kwargs.get('to','')
        start_lines = kwargs.get('start_lines',[])
        ending_lines=kwargs.get('ending_lines', [])
        links=kwargs.get('links', [])
        cc=kwargs.get('cc', '')
        bcc=kwargs.get('bcc', '')

        logger.info('recipients: {0}\nsubject: {1}\nbody:{2}'.format(
        to + ', ' + cc + ', ' + bcc, 
        subject, 
        '\n'.join(start_lines + ending_lines)
        ))
        return
    send_email(*args, **kwargs)


def send_email_celery(*args, **kwargs):
    if celery_up():
        send_email_async.delay(*args, **kwargs)
        return
    logger.warning("Celery workers are not active, trying to send email blocking!")
    send_email(*args, **kwargs)


# @celery_app.task
@shared_task()
def send_sms_async(*args, **kwargs):
    logger.info('start send sms')
    if settings.ENVIRONMENT_APP == 'DEVELOPE':
        logger.info('bypass send email in develop env')

        msisdn = kwargs.get('msisdn')
        body = kwargs.get('body')

        logger.info('msisdn: {0}\nbody: {1}'.format(msisdn, body))
        return
    send_sms(*args, **kwargs)


def send_sms_celery(*args, **kwargs):
    if celery_up():
        send_sms_async.delay(*args, **kwargs)
        return
    logger.warning("Celery workers are not active, trying to send sms blocking!")
    send_sms(*args, **kwargs)