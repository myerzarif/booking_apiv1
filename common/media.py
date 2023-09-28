from smtplib import SMTPException
import email.utils
import smtplib, ssl
from django.conf import settings
from django.template.loader import get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import logging

logger = logging.getLogger('project.media')


def send_email(*args, **kwargs):
    subject = kwargs.get('subject', '')
    to = kwargs.get('to','')
    title = kwargs.get('title', '')
    start_lines = kwargs.get('start_lines',[])
    table=kwargs.get('table', [])
    ending_lines=kwargs.get('ending_lines', [])
    links=kwargs.get('links', [])
    cc=kwargs.get('cc', '')
    bcc=kwargs.get('bcc', '')
    
    if type(to) == list:
        to = ', '.join(to)
    if type(cc) == list:
        cc = ', '.join(cc)
    if type(bcc) == list:
        bcc = ', '.join(bcc)
    if type(start_lines) == str:
        start_lines = start_lines.split('\n')
    if type(ending_lines) == str:
        ending_lines = ending_lines.split('\n')
    for row in table:
        row['values'] = row['value'].split('\n')
    mail_message = get_template('mail/mail.html').render({
        'title': title,
        'start_lines': start_lines,
        'table': table,
        'ending_lines': ending_lines,
        'links': links,
    })

    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject
    msg_root['From'] = email.utils.formataddr((settings.EMAIL_SENDER, settings.EMAIL_USERNAME))
    msg_root['To'] = to
    msg_root['Cc'] = cc
    msg_root['Bcc'] = bcc
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)

    msg_text = MIMEText(mail_message, 'html')
    msg_alternative.attach(msg_text)

    # fp = open('static/img/header-new.png', 'rb')
    # msg_header = MIMEImage(fp.read())
    # fp.close()
    # msg_header.add_header('Content-ID', '<header>')
    # msg_root.attach(msg_header)

    # fp = open('static/img/footer-new.png', 'rb')
    # msg_footer = MIMEImage(fp.read())
    # fp.close()
    # msg_footer.add_header('Content-ID', '<footer>')
    # msg_root.attach(msg_footer)

    try:
        tos = to.split(',')
        ccs = cc.split(',')
        bccs = bcc.split(',')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as smtp_server:
            smtp_server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            smtp_server.sendmail(settings.EMAIL_USERNAME, tos + ccs + bccs, msg_root.as_string())

        # with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
        #     smtp_server.connect(settings.EMAIL_HOST, settings.EMAIL_PORT)
        #     smtp_server.ehlo()
        #     smtp_server.starttls()
        #     smtp_server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        #     smtp_server.sendmail(settings.EMAIL_USERNAME, tos + ccs + bccs, msg_root.as_string())
        #     smtp_server.quit()
    except SMTPException as e:
        logger.error('Error: unable to send email to: {}'.format(to + ', ' + cc + ', ' + bcc), extra={
                    'error': str(e),
                }, exc_info=True)
    logger.info('recipients: {0}\nsubject: {1}\nbody:{2}'.format(
        to + ', ' + cc + ', ' + bcc,  subject , title ))


def send_sms(**kwargs):
    msisdn = kwargs.get('msisdn')
    body = kwargs.get('body')
    logger.info('msisdn: {0}\nbody: {1}'.format(msisdn, body))