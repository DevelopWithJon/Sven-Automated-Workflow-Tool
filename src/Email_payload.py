"""Catch updates from emails"""
from utils.configs import EMAILUSERNAME, EMAILPASSWORD
from utils.parse_excel import parse_orders
from retry import retry  # type: ignore

import email
import imaplib
import os
import time

import logging

cdir = os.getcwd()
attachment_path = cdir + "/attachments/"


logging.basicConfig(filename="example.log", encoding="utf-8")
LOGGER = logging.getLogger(__name__)


my_messaages = []
ATTACHMENT_EXT = (".xlsx", ".xls", ".csv")
SEEN = set()


def get_inbox(search_data, mail):

    for num in search_data[0].split():
        if num not in SEEN:
            LOGGER.info("server recieved new email")
            SEEN.add(num)
            print(SEEN)
            email_data = {}
            _, data = mail.fetch(num, "RFC822")
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ["subject", "to", "from", "date"]:
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data["body"] = body.decode()
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data["html_body"] = html_body.decode()
                if part.get_content_type() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue
                filename = part.get_filename()
                if filename:
                    if filename.endswith(ATTACHMENT_EXT):
                        if "attachments" in email_data:
                            email_data["attachments"] += [filename]
                        else:
                            email_data["attachments"] = [filename]
                        file_path = os.path.join(attachment_path + filename)
                        with open(file_path, "wb") as f:
                            f.write(part.get_payload(decode=True))
            my_messaages.append(email_data)
        else:
            return None
    return my_messaages


@retry(ValueError, delay=1, backoff=1.1, max_delay=10)
def await_new_email():

    host = "imap.gmail.com"
    username = EMAILUSERNAME
    password = EMAILPASSWORD

    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, password)
        mail.select("inbox")
    except:
        LOGGER.error("EMAILUSERNAME and EMAILPASSWORD should not be Null")
        mail.logout()
        raise AttributeError()

    _, search_data = mail.search(None, "UNSEEN", 'SUBJECT "New Order"')
    email_orders = get_inbox(search_data, mail)
    if email_orders:
        execute_order(email_orders)
        mail.close()
        mail.logout()

    else:
        LOGGER.info("server recieved nothing")
        print("server recieved nothing")
        mail.close()
        mail.logout()
        raise ValueError()


def execute_order(email_orders):
    LOGGER.info(f"grabbed {len(email_orders)} new email order(s)")
    for email_order in email_orders:
        LOGGER.info(f"parsing {email_order}")
        print(f"parsing {email_order}")
        parse_orders(email_order["attachments"])


if __name__ == "__main__":
    await_new_email()
    time.sleep(2)
    await_new_email()
