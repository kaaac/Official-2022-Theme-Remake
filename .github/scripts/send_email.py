#!/usr/bin/env python3
"""
Skrypt do wysyłania emaili z załącznikami przez Gmail SMTP
Używany przez GitHub Actions workflow
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
    Wysyła email z załącznikiem przez Gmail SMTP
    
    Args:
        to_email: Adres odbiorcy
        subject: Temat wiadomości
        body: Treść emaila
        attachment_path: Ścieżka do pliku załącznika
    """
    # Pobranie credentials z zmiennych środowiskowych
    from_email = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not from_email or not password:
        raise ValueError("Brak GMAIL_USER lub GMAIL_APP_PASSWORD w zmiennych środowiskowych")
    
    # Utworzenie wiadomości
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Dodanie treści
    msg.attach(MIMEText(body, 'plain'))
    
    # Dodanie załącznika
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
        print(f"✓ Załącznik dodany: {filename} ({os.path.getsize(attachment_path)} bytes)")
    else:
        print(f"⚠ Plik załącznika nie istnieje: {attachment_path}")
    
    # Wysłanie emaila
    try:
        print(f"Łączenie z smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"Logowanie jako {from_email}...")
        server.login(from_email, password)
        
        print(f"Wysyłanie do {to_email}...")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print(f"✓ Email wysłany pomyślnie do {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("✗ BŁĄD: Nieprawidłowe dane logowania Gmail")
        print("  Sprawdź czy App Password jest poprawny i czy 2FA jest włączone")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ BŁĄD SMTP: {e}")
        return False
    except Exception as e:
        print(f"✗ BŁĄD: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python send_email.py <adres_email> [ścieżka_załącznika]")
        sys.exit(1)
    
    recipient = sys.argv[1]
    attachment = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Możesz dostosować subject i body
    subject = "Twoja spersonalizowana paczka z repozytorium"
    body = """Cześć!

W załączniku znajdziesz spersonalizowaną paczkę z repozytorium.

Kod został dostosowany zgodnie z parametrami konfiguracyjnymi.

Pozdrawiam,
Automatyczny System Dystrybucji
"""
    
    success = send_email_with_attachment(
        to_email=recipient,
        subject=subject,
        body=body,
        attachment_path=attachment
    )
    
    sys.exit(0 if success else 1)
