import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
import random
import string

# Setup logging configuration
def setup_logger(log_file='logs/ids.log'):
    """
    Sets up a logger for logging IDS activities.
    """
    logger = logging.getLogger('IDSLogger')
    logger.setLevel(logging.INFO)
    
    # File handler to log messages to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler for displaying messages on console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Function to send alert emails
def send_alert_email(subject, message, config_file='config/config.yaml'):
    """
    Sends an alert email using SMTP server configuration from config file.
    """
    # Load configuration settings
    config = ConfigParser()
    config.read(config_file)
    
    smtp_server = config.get('email', 'smtp_server')
    smtp_port = config.getint('email', 'smtp_port')
    sender_email = config.get('email', 'sender_email')
    sender_password = config.get('email', 'sender_password')
    receiver_email = config.get('email', 'alert_receiver_email')
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Alert email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Function to log an alert
def log_alert(logger, message):
    """
    Logs an alert message to the logger.
    """
    logger.warning(message)

# Function to log informational messages
def log_info(logger, message):
    """
    Logs an informational message to the logger.
    """
    logger.info(message)

# Function to generate OTP
def generate_otp(length=6):
    """
    Generate a random OTP code.
    """
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

# Function to send OTP email
def send_otp_email(receiver_email, otp, config_file='config/config.yaml'):
    """
    Sends an OTP email to the receiver for verification.
    """
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"
    
    # Send the email using the same configuration
    return send_alert_email(subject, message, config_file)

# Function to register a user and send OTP
def register_user(email, config_file='config/config.yaml'):
    """
    Register a user by generating and sending an OTP to their email.
    """
    otp = generate_otp()
    if send_otp_email(email, otp, config_file):
        print(f"OTP sent to {email}")
        return otp  # Store this OTP securely for verification purposes
    else:
        print("Failed to send OTP.")
        return None

# Function to verify OTP
def verify_otp(input_otp, actual_otp):
    """
    Verifies the user-provided OTP against the actual OTP.
    """
    if input_otp == actual_otp:
        print("OTP verification successful.")
        return True
    else:
        print("Invalid OTP.")
        return False

# Example usage
if __name__ == "__main__":
    # Setup logger
    logger = setup_logger()
    
    # Example alert message
    log_info(logger, "Intrusion Detection System started.")
    
    # Example alert log
    log_alert(logger, "Suspicious network traffic detected from IP 192.168.1.100.")
    
    # Example email alert
    send_alert_email("IDS Alert", "Suspicious network traffic detected.")
    
    # Register a user
    email = "user@example.com"  # Replace with actual user email
    otp = register_user(email)
    
    # OTP verification process
    if otp:
        input_otp = input("Enter the OTP sent to your email: ")
        verify_otp(input_otp, otp)
