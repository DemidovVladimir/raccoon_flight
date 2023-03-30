import smtplib
import os
from dotenv import load_dotenv
load_dotenv(".env")

class PushNotifications:
    envs = os.environ.copy()
    my_email = ''
    email_password = ''
    connection = ''

    def __init__(self):
        self.connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.email_password = self.envs.get("EMAIL_PASSWORD")
        self.my_email = self.envs.get("MY_EMAIL")
    
    def send_email(self, subject, body):
        self.connection.starttls()
        self.connection.login(self.my_email, self.email_password)
        self.connection.sendmail(self.my_email, self.my_email, f"Subject: {subject}\n\n{body}")
        self.connection.close()

    def get_email(self):
        return self.my_email
