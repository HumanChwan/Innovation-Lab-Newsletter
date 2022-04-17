from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from terminal import ERROR, LOG, DEBUG


class Email:
    def __init__(self, login_email, login_password):
        self.LOGIN_EMAIL = login_email
        self.LOGIN_PASSWORD = login_password
        self.server = None

        # Checking if LOGIN_EMAIL AND LOGIN_PASSWORD exist
        if self.LOGIN_EMAIL is None or self.LOGIN_PASSWORD is None:
            ERROR(".env file doesn't exist or LOGIN_EMAIL or LOGIN_PASSWORD does not exist")
            raise ".ENV Does not exist"
        else:
            LOG(".env Found.")

    def __enter__(self):
        self.connect()
        return self

    def connect(self):
        # try to connect to the smtp server of gmail.
        try:
            self.server = SMTP("smtp.gmail.com", 587)
            self.server.starttls()
            LOG(self.server.noop())
        except SMTPConnectError as e:
            ERROR(e)
            return

        self._login()

    def _login(self):
        # try to log in to smtp server, with email credentials
        try:
            DEBUG(self.LOGIN_EMAIL, self.LOGIN_PASSWORD)
            self.server.login(self.LOGIN_EMAIL, self.LOGIN_PASSWORD)
        except SMTPAuthenticationError as e:
            ERROR(e)
            return

    def create_mail(self, to: str, html_template: str):
        # Forming the message
        msg = MIMEMultipart('alternative')
        # email's sender: 'inno-lab <email@email.com>'
        msg['From'] = f'inno-lab <{self.LOGIN_EMAIL}>'
        # email's recipient: accepted from the user
        msg['To'] = to
        # Setting the subject of the email
        msg['Subject'] = 'testing'

        # reading the content of the email from a local html file
        text = html = html_template

        # making MIME for text and html part
        text_part = MIMEText(text, 'text')
        html_part = MIMEText(html, 'html')

        # attaching the html and text part to email message
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()

    def send_mail(self, to: str, html_template: str):
        # try to send the email.
        try:
            self.server.sendmail(self.LOGIN_EMAIL, to, self.create_mail(to, html_template))
        except [SMTPDataError, SMTPRecipientsRefused] as e:
            ERROR(e)

    def close(self):
        # quitting the server connection
        self.server.quit()

    def __exit__(self, exit_type, value, traceback):
        self.close()

    def __str__(self):
        return f"Email class object corresponding to the email: {self.LOGIN_EMAIL}"

