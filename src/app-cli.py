import os
from dotenv import load_dotenv

from Email import Email
from terminal import ERROR, LOG

EMAIL_STORE_FILE = ""


def add_email_recipient():
    email = input("Enter Email to be added: ")
    with open(EMAIL_STORE_FILE, "r") as f:
        if email in map(lambda x: x.strip(), f.read().split('\n')):
            ERROR(f'Email: <{email}> already exists.')
            return

    with open(EMAIL_STORE_FILE, "a") as f:
        f.write(f'{email}\n')

    LOG("Email Added!")


def remove_email_recipient():
    email = input("Enter Email to be removed: ")
    with open(EMAIL_STORE_FILE, "r") as f:
        content = list(map(lambda x: x.strip(), f.read().split('\n')))
        try:
            content.remove(email)
        except ValueError:
            ERROR("This email does not exist.")
            return

    with open(EMAIL_STORE_FILE, "w") as f:
        f.write('\n'.join(content))

    LOG(f"Email <{email}> removed")


def send_mail_to_all_recipients(email: Email):
    with open(EMAIL_STORE_FILE, "r") as f:
        emails = list(map(lambda x: x.strip(), f.read().split('\n')))
        for email_address in emails:
            if email_address == "":
                continue
            email.send_mail(email_address)


def menu(email: Email):
    print("--------------------------------------")
    LOG("----Newsletter Admin Menu----")
    print("""
    1. Add an email recipient.
    2. Remove an email recipient.
    3. Send Mail to all email recipients.
    4. Exit.
    """)

    menu_option = input("Enter Option: ")
    if menu_option == '1':
        add_email_recipient()
    elif menu_option == '2':
        remove_email_recipient()
    elif menu_option == '3':
        send_mail_to_all_recipients(email)
    elif menu_option == '4':
        LOG("Closing...")
        return
    else:
        ERROR("Incorrect Input")

    menu(email)


def check_and_verify_store_file():
    if not os.path.isfile(EMAIL_STORE_FILE):
        LOG("Email store file not found, creating `src/data/emails.txt`")
        f = open(EMAIL_STORE_FILE, "x")
        f.close()


def main():
    global EMAIL_STORE_FILE
    # Getting login credentials from the .env file
    load_dotenv()
    login_email = os.getenv('LOGIN_EMAIL')
    login_password = os.getenv('LOGIN_PASSWORD')
    EMAIL_STORE_FILE = os.getenv('EMAIL_STORE_PATH')

    check_and_verify_store_file()

    with Email(login_email, login_password) as email:
        LOG("Connecting to SMTP server and starting TLS.")
        menu(email)
        LOG("Closing Connection to SMTP server")


if __name__ == "__main__":
    main()
