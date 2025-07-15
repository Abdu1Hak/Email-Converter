email_body = """Dear Irestify,

A new Service Issue has been assigned to you. Kindly contact the tenant, David Turner at this contact number: (647)229-1567 within one business day to schedule an appointment to address this work order.

Please note the tenant is also copied on this correspondence so we can connect you faster.

Secondary Tenant Info if applicable: N/A

Please be advised that your company is only authorized to attend to the service request listed in this work order. Any additional requests will need to be submitted by the tenant using the Tenant portal.

Summary of this Work Order:

Date Submitted: 07/07/2025  
Property Name & Address: The 88 on Broadway  
Suite: 1601  
Work Order Category: Plumbing  
Priority: Medium  
Work Order Subject:  
Work Order Description: Kitchen faucet handle got broken  
Troubleshooting Completed:  

Service Dispatch Tenant Disclaimer:

We ask that you please review and note the below terms of your visit:

- Please note that this service visit may be billed to the tenant dependent on the circumstance of the request, specifically in cases where cause of issue is determined to be result of tenant damage.
- It is the responsibility of the owner and/or property manager to service any regular maintenance or wear and tear items. Any service calls outside of these parameters will likely be billed to the requesting party.
- There is a minimum service fee of 2 hours per visit, that will be billed regardless of the scope of repair.
- Last minute cancellations, no show or refusal of entry will result in a cancellation fee of the 2 hour charge noted above.
- After hours and weekend service rates include additional fees.

By receipt of this notification you as the requesting party agree to the above terms and fees associated with your upcoming service visit.

Thank you,

Warm regards,  
Taiye Murtala  
Customer Service Specialist  
Del Condominium Rentals  
Member of the Tridel Group"""

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
    decoded = decode_header(subject)[0]
    if isinstance(decoded[0], bytes):
        return decoded[0].decode(decoded[1] or "utf-8")
    return decoded[0]

def get_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')

    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} unread email(s)")

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = clean_subject(msg["Subject"])
        sender = msg["From"]

        print(f"From: {sender}")
        print(f"Subject: {subject}")

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print(f"Body:\n{body}")
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            print(f"Body:\n{body}")
        
        print("=" * 50)

    mail.logout()


