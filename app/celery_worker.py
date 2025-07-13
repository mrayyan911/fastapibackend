from celery import Celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from app.services.verification_code_service import VerificationCodeService
from app.db.session import SessionLocal

# Initialize Celery with Redis as broker and backend
celery = Celery(
    'worker',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
)

@celery.task
def send_verification_email(email: str, user_id: int):
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

    # Generate verification code
    db = SessionLocal()
    verification_service = VerificationCodeService(db)
    verification_code_obj = verification_service.create_code(user_id)
    verification_code = verification_code_obj.code
    db.close()

    # Set up the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Email Verification'
    
    # Load the email template
    template_path = os.path.join(os.path.dirname(__file__), "email_templates", "welcome.html")
    with open(template_path, "r") as f:
        html_body = f.read()
    
    # Replace placeholder with actual verification code
    html_body = html_body.replace("{{verification_code}}", verification_code)

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