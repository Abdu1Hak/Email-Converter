from email_reader import get_unread_emails
from ai_extractor import extract_with_ai 
import schedule
import time

def job():
    emails = get_unread_emails()
    extract_with_ai(emails)

job()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


