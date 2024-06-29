import argparse
import os
import smtplib
from email import Encoders
from string import Template

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(smtp_server, from_addr, to_addr_list, cc_addr_list, subject, message, attachment_path):
    """
    Sends an email using the specified SMTP server.

    :param smtp_server: str - The SMTP server address used to send the email.
    :param from_addr: str - The email address of the sender.
    :param to_addr_list: list - A list of email addresses to send the email to.
    :param cc_addr_list: list - A list of email addresses to CC.
    :param subject: str - The subject line of the email.
    :param message: str - The body text of the email.
    :param attachment_path: str - The file path to an attachment (optional).

    :return: None
    """
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr_list)
    msg['Cc'] = ', '.join(cc_addr_list)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    if attachment_path and os.path.isfile(attachment_path):
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as f:
            part.set_payload(f.read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(os.path.basename(attachment_path)))
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server)
        to_addr_list = to_addr_list + cc_addr_list
        server.sendmail(from_addr, to_addr_list, msg.as_string())
        server.quit()
        print '[INFO] Email sent successfully.'
    except Exception as e:
        print '[ERROR] Failed to send email: {}'.format(e)


def get_template(tmpl_type, tmpl_data):
    """
    Returns the template content based on the type

    :param tmpl_type: str - Type of template ('pre' or 'post')
    :param tmpl_data: dict - Data to be used in the template
    :return: str - Template content
    """
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'templates', '{}_job.tmpl'.format(tmpl_type))
    if os.path.isfile(tmpl_path):
        with open(tmpl_path, 'r') as f:
            tmpl_obj = Template(f.read())
            return tmpl_obj.safe_substitute(**tmpl_data)
    return 'Template not found'


def main():
    """
    Main function

    :return: None
    """
    parser = argparse.ArgumentParser(description='Send Email')
    parser.add_argument('--host', help='SMTP server address', required=True)
    parser.add_argument('--from', dest='from_addr', help='Sender email address', required=True)
    parser.add_argument('--to', dest='to_addr', help='Recipient email addresses (comma-separated)', required=True)
    parser.add_argument('--cc', dest='cc_addr', help='CC email addresses (comma-separated)')
    parser.add_argument('--subject', help='Subject line of the email', required=True)
    parser.add_argument('--message', help='Body text of the email', default='No message body')
    parser.add_argument('--attachment', help='Path to an attachment file')
    parser.add_argument('--tmpl', choices=['pre', 'post'], help='Choose template to use')
    args = parser.parse_args()

    to_addr_list = args.to_addr.split(',')
    cc_addr_list = args.cc_addr.split(',') if args.cc_addr else []

    message = args.message
    if args.tmpl:
        tmpl_data_dict = {key: value for key, value in os.environ.items()}
        message = get_template(args.tmpl, tmpl_data_dict)

    send_email(smtp_server=args.host, from_addr=args.from_addr,
               to_addr_list=to_addr_list, cc_addr_list=cc_addr_list,
               subject=args.subject, message=message,
               attachment_path=args.attachment)


if __name__ == '__main__':
    main()
