import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# --- Settings ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SUBJECT = "Test Email from Python"
BODY = "This is a test email sent from a Python script!"

# --- Email setup ---
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = SUBJECT

msg.attach(MIMEText(BODY, 'plain'))

# --- Send email ---
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error sending email: {e}")
