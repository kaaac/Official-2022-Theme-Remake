#!/usr/bin/env python3
"""
Script for sending emails with attachments via Gmail SMTP
Used by GitHub Actions workflow
"""

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_email_with_attachment(to_email, subject, body, attachment_path):
    """
    Sends email with attachment via Gmail SMTP
    
    Args:
        to_email: Recipient address
        subject: Email subject
        body: Email body
        attachment_path: Attachment file path
    """
    # Pobranie credentials z zmiennych środowiskowych
    from_email = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not from_email or not password:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASSWORD in environment variables")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        msg.attach(part)
        print(f"✓ Attachment added: {filename} ({os.path.getsize(attachment_path)} bytes)")
    else:
        print(f"⚠ Attachment file does not exist: {attachment_path}")
    
    # Send email
    try:
        print(f"Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"Logging in as {from_email}...")
        server.login(from_email, password)
        
        print(f"Sending to {to_email}...")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print(f"✓ Email sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("✗ ERROR: Invalid Gmail credentials")
        print("  Check if App Password is correct and 2FA is enabled")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ SMTP ERROR: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Send email with package link or attachment')
    parser.add_argument('email', help='Recipient email address')
    parser.add_argument('attachment', nargs='?', help='Attachment file path (optional)')
    parser.add_argument('--link', help='Download link instead of attachment')
    parser.add_argument('--tag', help='Release tag for reference')
    
    args = parser.parse_args()
    
    recipient = args.email
    
    if args.link:
        # Send email with download link
        subject = "Your personalized package - Download Link"
        body = f"""Hello!

Your personalized package is ready for download.

🔗 Download Link:
{args.link}

⚠️ Important:
- This link is valid for 90 days
- For private repositories, you'll need GitHub access
- Package reference: {args.tag or 'N/A'}

If you have any issues accessing the package, please contact support.

Best regards,
Automated Distribution System"""
        
        # Send without attachment
        success = send_email_with_attachment(recipient, subject, body, None)
    else:
        # Original behavior with attachment
        attachment = args.attachment
        subject = "Your personalized package from repository"
        body = """Hello!

Please find attached your personalized package from the repository.

The code has been adjusted according to configuration parameters.

Best regards,
Automated Distribution System
"""
    
        success = send_email_with_attachment(
            to_email=recipient,
            subject=subject,
            body=body,
            attachment_path=attachment
        )
    
    sys.exit(0 if success else 1)
