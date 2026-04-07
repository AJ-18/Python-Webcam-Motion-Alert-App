import smtplib
import imghdr
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("APP_PASS")
SENDER = os.getenv("EMAIL_ADD")
RECEIVER = os.getenv("EMAIL_ADD")

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Object noticed!"
    email_message.set_content("Hey, just noticed an object appear!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/10.png")