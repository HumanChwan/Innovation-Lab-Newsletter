from typing import Union

import streamlit as st
import streamlit.components.v1 as components

from Email import Email
from config import config, get_email_store_path
from terminal import LOG, ERROR

success_colors = ["#095317", "#2e9e235e"]
error_colors = ["#530909", "#9e23235e"]
log_colors = ["rgb(61, 157, 243)", "rgba(28, 131, 225, 0.1)"]


def get_style(success: Union[bool, str], custom: str = ""):
    if type(success) == bool:
        colors = success_colors if success else error_colors
    elif success == "LOG":
        colors = log_colors
    return f'background: {colors[1]}; color: {colors[0]}; padding: 0.5rem 1rem; border: 1px solid {colors[0]}; ' \
           f'border-radius: 0.5rem; font-family: \'Source Sans Pro\', sans-serif; {custom}'


def add_email_recipient(email_store_path, email_address):
    with open(email_store_path, "r") as f:
        if email_address in map(lambda x: x.strip(), f.read().split('\n')):
            ERROR(f'Email: <{email_address}> already exists.')
            return False, f'Email <strong>{email_address}</strong> has already subscribed!'

    with open(email_store_path, "a") as f:
        f.write(f'{email_address}\n')

    return True, f'Email <strong>{email_address}</strong> Added!'


def remove_email_recipient(email_store_path, email_address):
    with open(email_store_path, "r") as f:
        content = list(map(lambda x: x.strip(), f.read().split('\n')))
        try:
            content.remove(email_address)
        except ValueError:
            ERROR("This email does not exist.")
            return False, f'Email <strong>{email_address}</strong> is not subscribed!'

    with open(email_store_path, "w") as f:
        f.write('\n'.join(content))

    LOG(f"Email <{email_address}> removed")
    return True, f'Email <strong>{email_address}</strong> removed!'


def send_mail_to_all_recipients(email_store_path):
    with config() as email:
        with open(email_store_path, "r") as f:
            emails = list(map(lambda x: x.strip(), f.read().split('\n')))
            for email_address in emails:
                if email_address == "":
                    continue
                LOG(email_address)
                email.send_mail(email_address)

    return True, 'Email(s) Sent!'


def read_all_emails(email_store_path):
    with open(email_store_path, "r") as f:
        return list(map(lambda x: x.strip(), f.read().split('\n')))


def main():
    email_store_path = get_email_store_path()
    st.title("Email Admin Interface")

    email_address_add = st.text_input(label='Add Email: ')
    add_email_button = st.button("Add Email")

    email_address_remove = st.text_input(label='Remove Email: ')
    remove_email_button = st.button('Remove Email')

    _, middle, _ = st.columns(3)
    send_email_button = middle.button('Send Email to all Recipients')
    show_all_emails = middle.button('Show all Emails')

    if add_email_button:
        if not email_address_add:
            components.html(f'<p style="{get_style(False)}">No email mentioned</p>')
            return
        success, message = add_email_recipient(email_store_path, email_address_add)
        components.html(f'<p style="{get_style(success)}">{message}</p>')
    elif remove_email_button:
        if not email_address_remove:
            components.html(f'<p style="{get_style(False)}">No email mentioned</p>')
            return
        success, message = remove_email_recipient(email_store_path, email_address_remove)
        components.html(f'<p style="{get_style(success)}">{message}</p>')
    elif show_all_emails:
        emails = read_all_emails(email_store_path)
        components.html(f'<p style="{get_style(len(emails) > 1)}"><strong>{len(emails) - 1}</strong>'
                        f' user(s) have Subscribed.</p>', height=60)
        if len(emails) > 1:
            st.write('\n'.join([f'{idx + 1}. {x}' for idx, x in enumerate(emails[:-1])]))
    elif send_email_button:
        components.html(f'<p style="{get_style("LOG")}">Please Wait...</p>', height=60)
        success, message = send_mail_to_all_recipients(email_store_path)
        components.html(f'<p style="{get_style(success)}">{message}</p>')


if __name__ == "__main__":
    main()
