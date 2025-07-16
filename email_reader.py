import os
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

def clean_subject(subject):
    if not subject:
        return "No Subject"
    
    decoded = decode_header(subject)[0]
    if isinstance(decoded[0], bytes):
        return decoded[0].decode(decoded[1] or "utf-8")
    return decoded[0]

def get_unread_emails():
    all_emails = []

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        if len(email_ids) == 0:
            mail.logout()
            return []

        for i, eid in enumerate(email_ids):
            try:
                status, msg_data = mail.fetch(eid, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = clean_subject(msg["Subject"])
                sender = msg["From"]

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":

                            try:
                                body = part.get_payload(decode=True).decode('utf-8')
                                break
                            except UnicodeDecodeError:

                                
                                try:
                                    body = part.get_payload(decode=True).decode('latin-1')
                                    break
                                except:
                                    body = "Could not decode email body"
                                    break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            body = msg.get_payload(decode=True).decode('latin-1')
                        except:
                            body = "Could not decode email body"
                
                total_message = f"From: {sender}\nSubject: {subject}\n\n{body}"
                all_emails.append(total_message)
                
            except Exception as e:
                continue

        mail.logout()
        
    except Exception as e:
        return []

    return all_emails