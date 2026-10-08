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
CONTACT_TO_EMAIL = os.getenv("ADMIN_EMAIL", NAMECHEAP_EMAIL)

# Simple in-memory rate limiter (best-effort, per instance).
# Key: sender email -> timestamp of last accepted submission.
_LAST_SUBMISSION = {}
_RATE_LIMIT_SECONDS = int(os.getenv("CONTACT_RATE_LIMIT_SECONDS", "60"))
_HONEYPOT_FIELD = os.getenv("CONTACT_HONEYPOT_FIELD", "website")

# Success / error pages used for no-JavaScript form submissions.
_PATHS = {
    "en": ("/contact/thanks/", "/contact/?error=1"),
    "es": ("/es/contact/gracias/", "/es/contact/?error=1"),
}

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


def _redirect(location: str) -> func.HttpResponse:
    return func.HttpResponse(status_code=303, headers={"Location": location})


def _respond(is_form: bool, lang: str, success: bool, message: str, status: int = 200) -> func.HttpResponse:
    """JSON for fetch() clients, a 303 redirect for native (no-JS) form posts."""
    if is_form:
        success_path, error_path = _PATHS.get(lang, _PATHS["en"])
        return _redirect(success_path if success else error_path)
    return func.HttpResponse(
        json.dumps({"success": success, "message": message}),
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
    content_type = (req.headers.get("content-type") or "").lower()
    is_form = "application/x-www-form-urlencoded" in content_type

    config_error = _validate_config()
    if config_error:
        if is_form:
            return _redirect(_PATHS["en"][1])
        return config_error

    if is_form:
        req_body = req.form
    else:
        try:
            req_body = req.get_json()
        except ValueError:
            return _error_response("Invalid request body")

    lang = (req_body.get("lang") or "en").strip().lower()
    if lang not in _PATHS:
        lang = "en"

    # Honeypot spam trap: real users never fill this hidden field.
    if req_body.get(_HONEYPOT_FIELD):
        return _respond(is_form, lang, True, "OK")

    name = (req_body.get("name") or "").strip()
    email = (req_body.get("email") or "").strip()
    subject = (req_body.get("subject") or "").strip()
    message = (req_body.get("message") or "").strip()

    if not name or not email or not subject or not message:
        return _respond(is_form, lang, False, "All fields are required", 400)
    if len(name) > MAX_NAME_LEN or len(email) > MAX_EMAIL_LEN or len(subject) > MAX_SUBJECT_LEN:
        return _respond(is_form, lang, False, "One or more fields exceed the maximum length", 400)
    if len(message) > MAX_MESSAGE_LEN:
        return _respond(is_form, lang, False, "Message is too long", 400)
    if not EMAIL_RE.match(email):
        return _respond(is_form, lang, False, "Please enter a valid email address", 400)

    # Basic rate limiting per sender email.
    now = time.time()
    last = _LAST_SUBMISSION.get(email, 0)
    if now - last < _RATE_LIMIT_SECONDS:
        return _respond(
            is_form, lang, False,
            "Please wait a moment before sending another message.", 429
        )
    _LAST_SUBMISSION[email] = now

    success, message_out = _send_email(name, email, subject, message)
    return _respond(is_form, lang, success, message_out, 200 if success else 500)
