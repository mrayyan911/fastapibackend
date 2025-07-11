from celery import Celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Initialize Celery with Redis as broker and backend
celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)
load_dotenv()
@celery_app.task
def send_verification_email(email: str):
    # Retrieve Gmail credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("GMAIL_APP_PASS")

    # Validate if environment variables are set
    if not sender_email or not password:
        print("Error: Missing Gmail credentials (SENDER_EMAIL or GMAIL_APP_PASSWORD).")
        return  # Exit early if credentials are not found

    # Ensure email is valid
    if not email:
        print("Error: No email provided.")
        return  # Exit early if email is None

    # Set up the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Email Verification'
    
    # Add the body of the email
    body = f"Please verify your email by clicking on the link: {email}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encrypt the connection
        server.login(sender_email, password)  # Log in with the Gmail app password
        server.sendmail(sender_email, email, msg.as_string())  # Send the email
        server.quit()  # Close the connection

        print(f"Verification email sent to {email}")
    except Exception as e:
        # Handle any errors and print them to the console
        print(f"Error sending email: {e}")