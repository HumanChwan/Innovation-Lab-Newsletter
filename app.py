import os

from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from terminal import DEBUG, ERROR, LOG


def main():
    # Getting login credentials from the .env file
    load_dotenv()
    LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
    LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')

    # Checking if LOGIN_EMAIL AND LOGIN_PASSWORD exist
    if LOGIN_EMAIL is None or LOGIN_PASSWORD is None:
        ERROR('.env file doesn\'t exist or LOGIN_EMAIL or LOGIN_PASSWORD does not exist')
        return 

    # try to connect to the smtp server of gmail.
    try:
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        LOG(server.noop())
    except SMTPConnectError as e:
        ERROR(e)
        return 

    # try to login to smtp server, with email credentials
    try:
        DEBUG(LOGIN_EMAIL, LOGIN_PASSWORD)
        server.login(LOGIN_EMAIL, LOGIN_PASSWORD)
    except SMTPAuthenticationError as e:
        ERROR(e)
        return 

    # Accepting Mail Recipient from user. 
    to = input('Enter the mail recipient: ')


    # Forming the message 
    msg = MIMEMultipart('alternative')
    # email's sender: 'inno-lab <email@email.com>'
    msg['From'] = f'inno-lab <{LOGIN_EMAIL}>'
    # email's recipient: accepted from the user
    msg['To'] = to
    # Setting the subject of the email
    msg['Subject'] = 'testing'

    # reading the content of the email from a local html file 
    text = html = open('./test.html', 'r').read()

    # making MIME for text and html part
    text_part = MIMEText(text, 'text')
    html_part = MIMEText(html, 'html')

    # attaching the html and text part to email message
    msg.attach(text_part)
    msg.attach(html_part)

    # try to send the email.
    try:
        server.sendmail(LOGIN_EMAIL, to, msg.as_string())
        LOG("Mail Sent!")
    except [SMTPDataError, SMTPRecipientsRefused] as e:
        ERROR(e)

    # quitting the server connection
    server.quit()


if __name__ == "__main__":
    main()
