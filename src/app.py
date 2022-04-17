from typing import Union

import streamlit as st
import streamlit.components.v1 as components

from jinja2 import Template
import json

from Email import Email
from config import config, get_email_store_path
from terminal import LOG, ERROR


success_colors = ["#095317", "#2e9e2322"]
error_colors = ["#530909", "#9e232322"]
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


def send_mail_to_all_recipients(email_store_path: str):
    with config() as email:
        with open(email_store_path, "r") as f:
            emails = list(map(lambda x: x.strip(), f.read().split('\n')))
            for email_address in emails:
                if email_address == "":
                    continue
                LOG(email_address)
                email.send_mail(email_address, get_news_template())

    return True, 'Email(s) Sent!'


def read_all_emails(email_store_path):
    with open(email_store_path, "r") as f:
        return list(map(lambda x: x.strip(), f.read().split('\n')))


def get_news_template():
    with open('data/news.html') as f:
        with open('data/data.json') as data_file:
            data_json = json.load(data_file)
            return Template(f.read()).render(news_objects=data_json['news_objects'])


def main():
    email_store_path = get_email_store_path()
    st.title("Email Admin Interface")

    email_address_add = st.text_input(label='Add Email: ')
    add_email_button = st.button("Add Email")

    email_address_remove = st.text_input(label='Remove Email: ')
    remove_email_button = st.button('Remove Email')

    # division of row into 3 divisions
    _, middle3, _ = st.columns(3)
    # division of row into 5 divisions
    _, _, middle5, _, _ = st.columns(5)

    send_email_button = middle3.button('Send Email to all Recipients')
    preview_email_button = middle3.button('Preview email to be sent')
    show_all_emails = middle5.button('Show all users')

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
        with st.expander('Email Recipients'):
            if len(emails) > 1:
                st.write('\n'.join([f'{idx + 1}. {x}' for idx, x in enumerate(emails[:-1])]))
    elif preview_email_button:
        with st.expander('data/news.html'):
            components.html(get_news_template(), height=500, scrolling=True)
    elif send_email_button:
        components.html(f'<p style="{get_style("LOG")}">Please Wait...</p>', height=60)
        success, message = send_mail_to_all_recipients(email_store_path)
        components.html(f'<p style="{get_style(success)}">{message}</p>')


if __name__ == "__main__":
    main()
