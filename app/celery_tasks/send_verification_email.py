
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from app.celery_config import celery_obj
from pathlib import Path
@celery_obj.task(name="send_verification_email")
def send_verification_email(email: str,verification_link: str):
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

    # Generate verification token
    
    

    # Set up the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Email Verification'
    
    # Load the email template
    #give the correct path to the template which is in app/email_templates/verify.html use robust method
    template_path = Path(__file__).resolve().parent.parent / 'email_templates' / 'verify.html'
    with open(template_path, "r") as f:
        html_body = f.read()
    
    # Replace placeholder with actual verification link
    html_body = html_body.replace("{{verification_link}}", verification_link)

    msg.attach(MIMEText(html_body, 'html'))

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