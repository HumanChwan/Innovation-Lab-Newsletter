import os

from Email import Email

from terminal import LOG


def check_and_verify_store_file(email_store_path: str):
    if not os.path.isfile(email_store_path):
        LOG("Email store file not found, creating `src/data/emails.txt`")
        f = open(email_store_path, "x")
        f.close()


def get_email_store_path():
    email_store_path = os.getenv('EMAIL_STORE_PATH')
    check_and_verify_store_file(email_store_path)
    return email_store_path


def config():
    login_email = os.getenv('LOGIN_EMAIL')
    login_password = os.getenv('LOGIN_PASSWORD')

    LOG("Connecting to SMTP and starting TLS")
    return Email(login_email, login_password)
