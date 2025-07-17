from email_reader import get_unread_emails
from ai_extractor import extract_with_ai 
import schedule
import time

counter = 1

def job():
    global counter
    emails = get_unread_emails()
    extract_with_ai(emails, counter)
    counter += 1

schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


