import azure.functions as func
import os
import json
import smtplib
import re
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# CONFIGURATION - Set these in Azure Function App Settings
# ============================================
NAMECHEAP_SMTP_SERVER = os.getenv("NAMECHEAP_SMTP_SERVER", "smtp.namecheap.com")
NAMECHEAP_SMTP_PORT = int(os.getenv("NAMECHEAP_SMTP_PORT", "587"))
NAMECHEAP_EMAIL = os.getenv("NAMECHEAP_EMAIL")
NAMECHEAP_PASSWORD = os.getenv("NAMECHEAP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", NAMECHEAP_EMAIL)
CONTACT_TO_EMAIL = os.getenv("CONTACT_TO_EMAIL", NAMECHEAP_EMAIL)

# Simple in-memory rate limiter (best-effort, per instance).
# Key: sender email -> timestamp of last accepted submission.
_LAST_SUBMISSION = {}
_RATE_LIMIT_SECONDS = int(os.getenv("CONTACT_RATE_LIMIT_SECONDS", "60"))
_HONEYPOT_FIELD = os.getenv("CONTACT_HONEYPOT_FIELD", "website")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_MESSAGE_LEN = 5000
MAX_NAME_LEN = 120
MAX_SUBJECT_LEN = 200
MAX_EMAIL_LEN = 254


def _error_response(message: str, status: int = 400) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"success": False, "message": message}),
        status_code=status,
        mimetype="application/json"
    )


def _validate_config() -> func.HttpResponse | None:
    if not NAMECHEAP_EMAIL or not NAMECHEAP_PASSWORD:
        return _error_response(
            "Server configuration incomplete. Contact administrator.",
            status=500
        )
    return None


def _send_email(name: str, sender: str, subject: str, message: str) -> tuple[bool, str]:
    """Send the contact message to the site owner via Namecheap SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Website Contact: {subject}"
        msg["From"] = FROM_EMAIL
        msg["To"] = CONTACT_TO_EMAIL
        msg["Reply-To"] = sender

        text = f"""
You have received a new message from your website contact form:

Name:    {name}
Email:   {sender}
Subject: {subject}

Message:
{message}
        """

        html = f"""\
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2>New website contact message</h2>
    <table style="border-collapse: collapse;">
      <tr><td style="font-weight: bold; padding: 4px 8px;">Name:</td>
          <td style="padding: 4px 8px;">{name}</td></tr>
      <tr><td style="font-weight: bold; padding: 4px 8px;">Email:</td>
          <td style="padding: 4px 8px;"><a href="mailto:{sender}">{sender}</a></td></tr>
      <tr><td style="font-weight: bold; padding: 4px 8px;">Subject:</td>
          <td style="padding: 4px 8px;">{subject}</td></tr>
    </table>
    <p style="font-weight: bold; margin-top: 20px;">Message:</p>
    <div style="padding: 12px; background: #f7f7f7; white-space: pre-wrap;">{message}</div>
  </body>
</html>
        """

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(NAMECHEAP_SMTP_SERVER, NAMECHEAP_SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD)
            server.sendmail(FROM_EMAIL, CONTACT_TO_EMAIL, msg.as_string())

        return True, "Message sent successfully"
    except Exception as e:
        return False, f"Email error: {str(e)}"


def main(req: func.HttpRequest) -> func.HttpResponse:
    config_error = _validate_config()
    if config_error:
        return config_error

    try:
        req_body = req.get_json()
    except ValueError:
        return _error_response("Invalid request body")

    # Honeypot spam trap: real users never fill this hidden field.
    if req_body.get(_HONEYPOT_FIELD):
        return func.HttpResponse("OK", status_code=200)

    name = req_body.get("name", "").strip()
    email = req_body.get("email", "").strip()
    subject = req_body.get("subject", "").strip()
    message = req_body.get("message", "").strip()

    if not name or not email or not subject or not message:
        return _error_response("All fields are required")
    if len(name) > MAX_NAME_LEN or len(email) > MAX_EMAIL_LEN or len(subject) > MAX_SUBJECT_LEN:
        return _error_response("One or more fields exceed the maximum length")
    if len(message) > MAX_MESSAGE_LEN:
        return _error_response("Message is too long")
    if not EMAIL_RE.match(email):
        return _error_response("Please enter a valid email address")

    # Basic rate limiting per sender email.
    now = time.time()
    last = _LAST_SUBMISSION.get(email, 0)
    if now - last < _RATE_LIMIT_SECONDS:
        return _error_response("Please wait a moment before sending another message.", status=429)
    _LAST_SUBMISSION[email] = now

    success, message_out = _send_email(name, email, subject, message)
    return func.HttpResponse(
        json.dumps({"success": success, "message": message_out}),
        status_code=200 if success else 500,
        mimetype="application/json"
    )
