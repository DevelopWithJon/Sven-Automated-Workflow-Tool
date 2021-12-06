"""Catch updated from emails"""
from configs import EMAILUSERNAME, EMAILPASSWORD

import imaplib
import email
import os

host = 'imap.gmail.com'
username = EMAILUSERNAME
password = EMAILPASSWORD

mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)
mail.select("inbox")

my_messaages = []
ATTACHMENT_EXT = (".xlsx",".xls",".csv")

_, search_data = mail.search(None, 'SEEN')

def get_inbox():
    
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, 'RFC822')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
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
                        email_data["attachments"]+=[filename]
                    else:
                        email_data["attachments"] = [filename]
                    # with open(filename,'wb') as f:
                    #     f.write(part.get_payload(decode=True))
        my_messaages.append(email_data)
    return my_messaages
        
def search_mesg(key, value, con):
    _, data = con.search(None, key, '"{}"'.format(value))

    return data

def get_attachments():
    pass
print(get_inbox())
#print(search_mesg("SUBJECT","info",mail))